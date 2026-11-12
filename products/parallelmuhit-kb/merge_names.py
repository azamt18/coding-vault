#!/usr/bin/env python3
"""
Merge names across the 188 essays into one graph (task 04).

Persons, works and organizations that are the same real thing become one node,
however the essays spell them. Ideas merge on an exact (casefolded) base_name only.

  1. split compound names ("Buffet va Munger") when every part is a known entity
  2. block candidate names in code (normalized spelling, last token, difflib)
  3. sonnet clusters each block via `claude -p` (extract.run_claude_cli), cached
  4. the label is the spelling used in the most essays (tie: the longer one)
  5. merge_overrides.json (merge / keep_apart / label) applies on every run
  6. graph.json: nodes, quoted links, wrote and mentioned_in built by code
  7. merge_summary.md for the user to skim and write overrides

Usage:
    python3 merge_names.py --jobs 3        # calls the model for uncached blocks
    python3 merge_names.py --offline       # rebuild from extract/merge/raw/ only

Reads extract/sonnet/*.json (never rewritten). Writes extract/merge/ and extract/graph.json.
"""

import argparse
import difflib
import hashlib
import json
import random
import re
import sys
import threading
import unicodedata
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import BaseModel, ValidationError

import extract

HERE = Path(__file__).resolve().parent
OVERRIDES_FILE = HERE / "merge_overrides.json"
MERGED_TYPES = ["person", "work", "organization"]
MAX_BLOCK = 40
RATIO = 0.8
SAMPLE_SEED = 20261112
SAMPLE_SIZE = 30
AUTHOR_ID = "author:" + "aziz-rahimov"

_APOSTROPHES = "‘ʻ'’`ʼ"
_COMPOUND = re.compile(r"\s+va\s+|\s*&\s*|\s+hamda\s+|\s*,\s*")

SYSTEM = """\
You group spellings of names from Uzbek essays by Aziz Rahimov. Each group is one real-world
person, work or organization. All names you get are of the same type and look alike.

Rules:
- Merge only when it is clearly the same real-world thing (different transliterations,
  "Charli Munger" / "Charlie Manger", a typo, a name with or without a first name).
- When unsure, keep them apart. Merging two different things is worse than leaving a duplicate.
- A surname alone ("Munger") merges with a full name only if the descriptions agree.
- Different people with the same surname (a father and a son, two authors) stay apart.

Reply with only one JSON object, no prose before or after it, no code fences:
{"clusters": [["name", "name", ...], ...]}
Use the names exactly as given. Each given name appears in at most one cluster.
A name that belongs with no other may be left out.
"""


class BadJsonError(extract.BadJson):
    pass


class ClustersOut(BaseModel):
    clusters: list[list[str]]


# --- normalization and blocking ---


def _fold_token(tok: str) -> str:
    for a, b in (("ye", "e"), ("oo", "u"), ("ks", "x"), ("y", "i")):
        tok = tok.replace(a, b)
    tok = re.sub(r"(.)\1+", r"\1", tok)
    if len(tok) > 2 and tok.endswith("e"):
        tok = tok[:-1]
    return tok


def normalize(name: str) -> str:
    """Spelling-blind form for blocking only (never shown, never used as a label)."""
    s = name.casefold()
    for ch in _APOSTROPHES:
        s = s.replace(ch, "")
    return " ".join(_fold_token(t) for t in s.split())


class _UnionFind:
    def __init__(self, items):
        self.parent = {x: x for x in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[max(ra, rb)] = min(ra, rb)


def _cap(block: list[str]) -> list[list[str]]:
    if len(block) <= MAX_BLOCK:
        return [block]
    by_letter = defaultdict(list)
    for n in block:
        last = (normalize(n).split() or [""])[-1]
        by_letter[last[:1]].append(n)
    out = []
    for _, group in sorted(by_letter.items()):
        group = sorted(group)
        out += [group[i:i + MAX_BLOCK] for i in range(0, len(group), MAX_BLOCK)]
    return out


def build_blocks(names: list[str]) -> list[list[str]]:
    """Group look-alike names (one type) with union-find. Every name is in exactly one block."""
    names = sorted(set(names))
    norm = {n: normalize(n) for n in names}
    uf = _UnionFind(names)
    by_last = defaultdict(list)
    for n in names:
        if norm[n]:
            by_last[norm[n].split()[-1]].append(n)
    for group in by_last.values():
        for other in group[1:]:
            uf.union(group[0], other)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            sm = difflib.SequenceMatcher(None, norm[a], norm[b])
            if sm.real_quick_ratio() >= RATIO and sm.quick_ratio() >= RATIO and sm.ratio() >= RATIO:
                uf.union(a, b)
    groups = defaultdict(list)
    for n in names:
        groups[uf.find(n)].append(n)
    blocks = []
    for g in groups.values():
        blocks += _cap(sorted(g))
    return sorted(blocks, key=lambda b: (b[0], len(b)))


@dataclass
class Block:
    type: str
    names: list[str]

    def __post_init__(self):
        self.names = sorted(self.names)

    @property
    def id(self) -> str:
        digest = hashlib.sha1("\n".join(self.names).encode("utf-8")).hexdigest()[:12]
        return f"{self.type}_{digest}"


# --- compound names ---


def _compound_parts(base: str) -> list[str]:
    parts = [p.strip() for p in _COMPOUND.split(base)]
    return parts if len(parts) >= 2 and all(parts) else []


def split_compounds(results: list[dict]) -> tuple[list[dict], dict]:
    """Split "A va B" into A and B when both are known entities of the same type. Input is not changed."""
    known = set()
    for r in results:
        for e in r["entities"]:
            if e["type"] in MERGED_TYPES and not _compound_parts(e["base_name"]):
                known.add((e["type"], e["base_name"].casefold()))

    stats = {"splits": 0, "copied_links": 0}
    out = []
    for r in results:
        r = json.loads(json.dumps(r))  # deep copy
        replace = {}  # compound name -> [part entity names]
        ents = list(r["entities"])
        for e in r["entities"]:
            parts = _compound_parts(e["base_name"]) if e["type"] in MERGED_TYPES else []
            if not parts or not all((e["type"], p.casefold()) in known for p in parts):
                continue
            part_names = []
            for p in parts:
                existing = next((x for x in ents if x["type"] == e["type"] and x is not e
                                 and x["base_name"].casefold() == p.casefold()), None)
                if existing is None:
                    existing = {**e, "name": p, "base_name": p, "aliases": []}
                    ents.append(existing)
                part_names.append(existing["name"])
            ents.remove(e)
            replace[e["name"]] = part_names
            stats["splits"] += 1
        if replace:
            rels = []
            for x in r["relations"]:
                sources = replace.get(x["source"], [x["source"]])
                targets = replace.get(x["target"], [x["target"]])
                copies = [{**x, "source": s, "target": t} for s in sources for t in targets]
                stats["copied_links"] += len(copies) - 1
                rels += copies
            r["relations"] = rels
            r["entities"] = ents
        out.append(r)
    return out, stats


# --- names per type ---


def collect_names(results: list[dict]) -> dict[tuple[str, str], dict]:
    """(type, casefolded base_name) -> spellings with their essays, verbatim names, a description and a quote."""
    info: dict[tuple[str, str], dict] = {}
    for r in results:
        eid = r["essay"]["id"]
        quotes = {}
        for x in r["relations"]:
            for end in (x["source"], x["target"]):
                quotes.setdefault(end, x["quote"])
        for e in r["entities"]:
            key = (e["type"], e["base_name"].casefold())
            d = info.setdefault(key, {"type": e["type"], "spellings": defaultdict(set), "names": set(),
                                      "descriptions": {}, "quote": "", "mentions": 0})
            d["spellings"][e["base_name"]].add(eid)
            d["names"].add(e["name"])
            d["descriptions"].setdefault(eid, e["description"])
            d["mentions"] += len(e["paragraphs"])
            if not d["quote"]:
                d["quote"] = quotes.get(e["name"], "")
    for d in info.values():
        d["display"], _ = choose_label(d["spellings"])
        d["essays"] = sorted(set().union(*d["spellings"].values()))
    return info


def choose_label(spellings: dict[str, set], extra_names=frozenset()) -> tuple[str, list[str]]:
    """The spelling in the most essays; on a tie the longer one. Everything else is an alias."""
    label = max(spellings, key=lambda s: (len(spellings[s]), len(s), s))
    aliases = sorted((set(spellings) | set(extra_names)) - {label})
    return label, aliases


# --- clustering a block ---


def parse_clusters(text: str, block_names: list[str]) -> tuple[list[list[str]], int]:
    """Clusters from the model's json. A cluster naming anything outside the block, or a name
    already used, is rejected whole (its names stay unmerged). Unused names become singletons."""
    try:
        out = ClustersOut.model_validate_json(text)
    except ValidationError as exc:
        raise BadJsonError(str(exc).splitlines()[0]) from exc
    allowed = set(block_names)
    used: set[str] = set()
    clusters, rejected = [], 0
    for c in out.clusters:
        members = list(dict.fromkeys(c))
        if not members:
            continue
        if any(m not in allowed for m in members) or any(m in used for m in members):
            rejected += 1
            continue
        used.update(members)
        clusters.append(members)
    clusters += [[n] for n in sorted(allowed - used)]
    return clusters, rejected


def cluster_prompt(block: Block, info: dict[str, dict]) -> str:
    lines = [f"Type: {block.type}", "", "Names (name | essays | description | sample quote):"]
    for n in block.names:
        d = info[n]
        lines.append(f'- {n} | {d["essays"]} | {d["description"]} | "{d["quote"]}"')
    return "\n".join(lines)


def cluster_block(block: Block, info: dict[str, dict], out_dir: Path, force: bool, offline: bool,
                  stats: dict | None = None) -> tuple[list[list[str]], str]:
    """(clusters, status) for one block; status is ok, no_raw or bad_json. Raises extract.CliError."""
    raw_path = out_dir / "raw" / f"{block.id}.json"
    if raw_path.exists() and not force:
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
    elif offline:
        return [[n] for n in block.names], "no_raw"
    else:
        raw = extract.run_claude_cli(extract.MODELS["sonnet"], SYSTEM, cluster_prompt(block, info))
        raw["block"] = {"type": block.type, "names": block.names}
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        clusters, rejected = parse_clusters(extract.response_text(raw), block.names)
    except BadJsonError:
        return [[n] for n in block.names], "bad_json"
    if stats is not None:
        stats["rejected_clusters"] = stats.get("rejected_clusters", 0) + rejected
    return clusters, "ok"


# --- overrides ---


@dataclass
class Cluster:
    type: str
    members: list[str]  # display names (one per casefolded base_name)
    label_override: str | None = None
    source: str = field(default="model")


def apply_overrides(clusters: list[Cluster], overrides: dict) -> tuple[list[Cluster], list[str]]:
    clusters = [Cluster(c.type, list(c.members), c.label_override, c.source) for c in clusters]
    warnings = []

    def find(name: str) -> Cluster | None:
        return next((c for c in clusters if any(m.casefold() == name.casefold() for m in c.members)), None)

    for group in overrides.get("merge", []):
        found = [(n, find(n)) for n in group]
        for n, c in found:
            if c is None:
                warnings.append(f"merge: unknown name {n!r}")
        targets = list(dict.fromkeys(id(c) for _, c in found if c is not None))
        hits = [c for c in clusters if id(c) in targets]
        if len({c.type for c in hits}) > 1:
            warnings.append(f"merge: {group} spans more than one type, skipped")
            continue
        if len(hits) > 1:
            keep = hits[0]
            for other in hits[1:]:
                keep.members = sorted(set(keep.members) | set(other.members))
                keep.label_override = keep.label_override or other.label_override
                clusters.remove(other)
            keep.source = "override"

    for group in overrides.get("keep_apart", []):
        for n in group:
            if find(n) is None:
                warnings.append(f"keep_apart: unknown name {n!r}")
        names = [n for n in group if find(n) is not None]
        for c in list(clusters):
            listed = [m for m in c.members if any(m.casefold() == n.casefold() for n in names)]
            for m in listed[1:]:
                c.members.remove(m)
                clusters.append(Cluster(c.type, [m], None, "override"))

    for name, label in overrides.get("label", {}).items():
        c = find(name)
        if c is None:
            warnings.append(f"label: unknown name {name!r}")
        else:
            c.label_override = label
    return clusters, warnings


# --- graph ---


def slug(text: str) -> str:
    s = unicodedata.normalize("NFKD", text.casefold())
    s = "".join(ch for ch in s if not unicodedata.combining(ch) and ch not in _APOSTROPHES)
    return re.sub(r"[^\w]+", "-", s).strip("-_") or "x"


def build_graph(results: list[dict], clusters: list[Cluster]) -> tuple[dict, dict]:
    info = collect_names(results)
    groups: list[tuple[str, list[tuple[str, str]], str | None]] = []
    covered = set()
    for c in clusters:
        keys = [(c.type, m.casefold()) for m in c.members if (c.type, m.casefold()) in info]
        if keys:
            groups.append((c.type, keys, c.label_override))
            covered.update(keys)
    for key in sorted(info):
        if key not in covered:  # ideas, and any name the clusters don't mention
            groups.append((key[0], [key], None))

    nodes, key_to_id, used_ids = [], {}, Counter()
    for etype, keys, label_override in sorted(groups, key=lambda g: (g[0], sorted(g[1]))):
        spellings = defaultdict(set)
        names, descriptions, mentions = set(), {}, 0
        for k in keys:
            d = info[k]
            for s, essays in d["spellings"].items():
                spellings[s] |= essays
            names |= d["names"]
            for eid, desc in d["descriptions"].items():
                descriptions.setdefault(eid, desc)
            mentions += d["mentions"]
        label, aliases = choose_label(spellings, names)
        if label_override:
            aliases = sorted((set(aliases) | {label}) - {label_override})
            label = label_override
        node_id = f"{etype}:{slug(label)}"
        used_ids[node_id] += 1
        if used_ids[node_id] > 1:
            node_id = f"{node_id}-{used_ids[node_id]}"
        for k in keys:
            key_to_id[k] = node_id
        nodes.append({"id": node_id, "label": label, "type": etype, "aliases": aliases,
                      "descriptions": dict(sorted(descriptions.items())),
                      "essays": sorted(set().union(*spellings.values())), "mention_count": mentions})

    nodes.append({"id": AUTHOR_ID, "label": extract.AUTHOR, "type": "author"})
    links, stats = [], {"self_loops": 0, "unresolved": 0, "relation_links": 0}
    for r in sorted(results, key=lambda r: r["essay"]["id"]):
        e = r["essay"]
        eid = e["id"]
        essay_id = f"essay:{eid}"
        nodes.append({"id": essay_id, "label": e["title"], "type": "essay", "number": e["number"],
                      "slug": e["slug"], "source": e["source"]})
        links.append({"source": AUTHOR_ID, "target": essay_id, "kind": "wrote", "essay": eid})
        by_name = {x["name"]: key_to_id[(x["type"], x["base_name"].casefold())] for x in r["entities"]}
        by_name[extract.AUTHOR] = AUTHOR_ID
        for x in r["relations"]:
            s, t = by_name.get(x["source"]), by_name.get(x["target"])
            if s is None or t is None:
                stats["unresolved"] += 1
                continue
            if s == t:
                stats["self_loops"] += 1
                continue
            links.append({"source": s, "target": t, "kind": x["kind"], "label": x["label"], "essay": eid,
                          "paragraph": x["paragraph"], "quote": x["quote"]})
            stats["relation_links"] += 1
        mentioned = defaultdict(set)
        for x in r["entities"]:
            mentioned[by_name[x["name"]]].update(x["paragraphs"])
        for node_id in sorted(mentioned):
            links.append({"source": node_id, "target": essay_id, "kind": "mentioned_in", "essay": eid,
                          "paragraphs": sorted(mentioned[node_id], key=lambda p: int(p[1:]))})
    nodes.sort(key=lambda n: n["id"])
    return {"nodes": nodes, "links": links}, stats


# --- summary ---


def render_summary(results, split_stats, info, clusters, graph, gstats, run_stats, warnings) -> str:
    before = Counter(e["type"] for r in results for e in r["entities"])
    distinct = Counter(t for t, _ in info)
    after = Counter(n["type"] for n in graph["nodes"])
    by_id = {n["id"]: n for n in graph["nodes"]}
    merged = sorted((n for n in graph["nodes"] if n["type"] in MERGED_TYPES and n["aliases"]
                     and len({a.casefold() for a in [n["label"], *n["aliases"]]}) > 1),
                    key=lambda n: n["id"])
    multi = [n for n in merged if len(_spellings_of(n, info)) > 1]

    out = ["# merge summary", "", "## counts", "",
           "| type | entities (rows) | distinct base_names | nodes |", "|---|---|---|---|"]
    for t in [*MERGED_TYPES, "idea"]:
        out.append(f"| {t} | {before[t]} | {distinct[t]} | {after[t]} |")
    out += ["",
            f"- compound names split: {split_stats['splits']}, links copied: {split_stats['copied_links']}",
            f"- self-loops dropped: {gstats['self_loops']}",
            f"- unresolved link endpoints: {gstats['unresolved']}",
            f"- blocks: {run_stats['blocks']} ({run_stats['singletons']} singletons, {run_stats['called']} sent to the model)",
            f"- rejected clusters: {run_stats.get('rejected_clusters', 0)}",
            f"- bad_json blocks: {len(run_stats['bad_json'])}" + (f" ({', '.join(run_stats['bad_json'])})" if run_stats["bad_json"] else ""),
            f"- blocks without a cached answer (offline): {len(run_stats['no_raw'])}",
            f"- relation links in the graph: {gstats['relation_links']}",
            ""]
    out += ["## override warnings", ""] + ([f"- {w}" for w in warnings] or ["none"]) + [""]

    out += ["## known variants", ""]
    for pat in ("munger|manger", "taleb", "buffet|baffet"):
        hits = [n for n in graph["nodes"] if n["type"] == "person"
                and re.search(pat, " ".join([n["label"], *n["aliases"]]).casefold())]
        out.append(f"- {pat}: " + "; ".join(f"{n['label']} ({', '.join(n['aliases'])})" for n in hits))
    out.append("")

    out += ["## 20 largest clusters", ""]
    for n in sorted(multi, key=lambda n: (-len(_spellings_of(n, info)), n["id"]))[:20]:
        out.append(f"- {n['label']} [{n['type']}, {len(n['essays'])} essays]: {', '.join(_spellings_of(n, info))}")
    out.append("")

    sample = sorted(random.Random(SAMPLE_SEED).sample(multi, min(SAMPLE_SIZE, len(multi))), key=lambda n: n["id"])
    out += [f"## {len(sample)} random merges to check (seed {SAMPLE_SEED})", ""]
    out += [_merge_line(n, info) for n in sample] + [""]

    out += [f"## all merges ({len(multi)})", "", "one line per node: label ← every base_name merged into it", ""]
    out += [_merge_line(n, info) for n in multi]
    return "\n".join(out) + "\n"


def _spellings_of(node: dict, info: dict) -> list[str]:
    forms = {a.casefold() for a in [node["label"], *node["aliases"]]}
    keys = [k for k in info if k[0] == node["type"] and k[1] in forms]
    return sorted(info[k]["display"] for k in keys)


def _merge_line(node: dict, info: dict) -> str:
    descs = list(node["descriptions"].values())[:2]
    return f"- {node['label']} [{node['type']}] ← {', '.join(_spellings_of(node, info))} — " + " / ".join(descs)


# --- running ---


def run_blocks(blocks: list[Block], info_by_type: dict, out_dir: Path, force: bool, offline: bool, jobs: int):
    stop = threading.Event()
    lock = threading.Lock()
    stats = {"rejected_clusters": 0}

    def work(block: Block):
        if stop.is_set():
            return block, [[n] for n in block.names], "not_started"
        try:
            clusters, status = cluster_block(block, info_by_type[block.type], out_dir, force, offline, stats)
        except extract.CliError as exc:
            stop.set()
            with lock:
                print(f"{block.id}: ERROR cli_error: {exc}; no new calls", file=sys.stderr, flush=True)
            return block, [[n] for n in block.names], "cli_error"
        if status != "ok":
            with lock:
                print(f"{block.id}: {status}", file=sys.stderr, flush=True)
        return block, clusters, status

    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        outcomes = list(pool.map(work, blocks))
    return outcomes, stats


def load_results(sonnet_dir: Path) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(sonnet_dir.glob("[0-9][0-9][0-9]_*.json"))]


def main():
    parser = argparse.ArgumentParser(description="Merge names across essays into extract/graph.json")
    parser.add_argument("--extract-dir", type=Path, default=extract.DEFAULT_OUT_DIR)
    parser.add_argument("--overrides", type=Path, default=OVERRIDES_FILE)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--force", action="store_true", help="call the model even for cached blocks")
    parser.add_argument("--offline", action="store_true", help="use cached answers only; never call the model")
    args = parser.parse_args()

    out_dir = args.extract_dir / "merge"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = load_results(args.extract_dir / "sonnet")
    split, split_stats = split_compounds(results)
    info = collect_names(split)

    blocks, singles, info_by_type = [], [], {}
    for t in MERGED_TYPES:
        names = {d["display"]: d for k, d in info.items() if k[0] == t}
        info_by_type[t] = {n: {"description": next(iter(d["descriptions"].values()), ""),
                               "essays": len(d["essays"]), "quote": d["quote"]} for n, d in names.items()}
        for b in build_blocks(list(names)):
            (blocks if len(b) > 1 else singles).append(Block(t, b))

    outcomes, run_stats = run_blocks(blocks, info_by_type, out_dir, args.force and not args.offline,
                                     args.offline, args.jobs)
    statuses = Counter(status for _, _, status in outcomes)
    run_stats.update({"blocks": len(blocks) + len(singles), "singletons": len(singles), "called": len(blocks),
                      "bad_json": sorted(b.id for b, _, s in outcomes if s == "bad_json"),
                      "no_raw": sorted(b.id for b, _, s in outcomes if s == "no_raw")})
    (out_dir / "blocks.json").write_text(json.dumps(
        [{"id": b.id, "type": b.type, "names": b.names} for b in blocks + singles], ensure_ascii=False, indent=1),
        encoding="utf-8")
    if statuses.get("cli_error") or statuses.get("not_started"):
        print(f"stopped: cli_error {statuses.get('cli_error', 0)}, not started {statuses.get('not_started', 0)}. "
              "rerun later without --force to resume; graph.json not written.", file=sys.stderr)
        sys.exit(1)

    clusters = [Cluster(b.type, c) for b, cs, _ in outcomes for c in cs] + [Cluster(b.type, list(b.names)) for b in singles]
    overrides = json.loads(args.overrides.read_text(encoding="utf-8")) if args.overrides.exists() else {}
    clusters, warnings = apply_overrides(clusters, overrides)
    for w in warnings:
        print(f"override warning: {w}", file=sys.stderr)
    (out_dir / "clusters.json").write_text(json.dumps(
        sorted(({"type": c.type, "members": sorted(c.members), "label_override": c.label_override, "source": c.source}
                for c in clusters if len(c.members) > 1), key=lambda c: (c["type"], c["members"])),
        ensure_ascii=False, indent=1), encoding="utf-8")

    graph, gstats = build_graph(split, clusters)
    (args.extract_dir / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "merge_summary.md").write_text(
        render_summary(split, split_stats, info, clusters, graph, gstats, run_stats, warnings), encoding="utf-8")
    after = Counter(n["type"] for n in graph["nodes"])
    print(f"graph.json: {len(graph['nodes'])} nodes ({dict(after)}), {len(graph['links'])} links; "
          f"self-loops {gstats['self_loops']}, unresolved {gstats['unresolved']}, bad_json {len(run_stats['bad_json'])}, "
          f"no_raw {len(run_stats['no_raw'])}")


if __name__ == "__main__":
    main()
