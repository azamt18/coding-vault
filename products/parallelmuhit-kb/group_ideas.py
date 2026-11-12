#!/usr/bin/env python3
"""
Group ideas (task 05): merge idea variants, then put the merged ideas under 5-15 themes.

Only ideas in 2+ essays take part; every other idea passes through unchanged, with no theme.

  1. select idea nodes from extract/graph.json with len(essays) >= 2
  2. sonnet clusters variants of the same idea via `claude -p` (one call if they fit), cached
  3. the label is the member label used in the most essays (tie: the longer one)
  4. idea_overrides.json (merge / keep_apart / label / theme) applies on every run
  5. sonnet puts the merged ideas under themes (one call), cached
  6. extract/graph_grouped.json: merged ideas, repointed links, theme nodes and in_theme links
  7. extract/ideas/ideas_summary.md for the user to skim and write overrides

Usage:
    python3 group_ideas.py             # calls the model for uncached answers
    python3 group_ideas.py --offline   # rebuild from extract/ideas/raw/ only

Reads extract/graph.json (never rewritten). Writes extract/ideas/ and extract/graph_grouped.json.
"""

import argparse
import hashlib
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

from pydantic import BaseModel, ValidationError

import extract
import merge_names as mn

HERE = Path(__file__).resolve().parent
OVERRIDES_FILE = HERE / "idea_overrides.json"
MIN_ESSAYS = 2
ONE_CALL_MAX = 150  # ideas per merge call; above this, blocks of MAX_BLOCK by first letter
MAX_BLOCK = 40
OTHER_THEME = "boshqa"
SAMPLE_SEED = mn.SAMPLE_SEED
SAMPLE_SIZE = 20

BadJsonError = mn.BadJsonError

MERGE_SYSTEM = """\
You group ideas from Uzbek essays by Aziz Rahimov. Each idea comes with its label, other
spellings, how many essays mention it and one short description per essay.

Rules:
- Merge only when two labels are the same idea (a spelling variant, a synonym used the same way,
  "SI" and "Sun'iy intellekt"). Related or opposite ideas stay apart ("Moliyaviy erkinlik" and
  "moliyaviy qaramlik" are two ideas). A broader topic is not the same idea as a narrower one.
- When unsure, keep them apart. Merging two different ideas is worse than leaving a duplicate.

Reply with only one JSON object, no prose before or after it, no code fences:
{"clusters": [["label", "label", ...], ...]}
Use the labels exactly as given. Each label appears in at most one cluster.
A label that belongs with no other may be left out.
"""

THEMES_SYSTEM = f"""\
You sort ideas from Uzbek essays by Aziz Rahimov into broader themes.

Rules:
- Make 5 to 15 themes. Each theme has a short Uzbek name (1-3 words, Latin script).
- Every given idea goes into exactly one theme.
- An idea that fits no theme goes into a theme named "{OTHER_THEME}".

Reply with only one JSON object, no prose before or after it, no code fences:
{{"themes": [{{"name": "theme name", "ideas": ["label", "label", ...]}}, ...]}}
Use the idea labels exactly as given.
"""


class ThemeOut(BaseModel):
    name: str
    ideas: list[str]


class ThemesOut(BaseModel):
    themes: list[ThemeOut]


# --- selection ---


def select_ideas(graph: dict) -> tuple[list[dict], list[dict]]:
    """(ideas in MIN_ESSAYS+ essays, the other ideas), both sorted by id."""
    ideas = sorted((n for n in graph["nodes"] if n["type"] == "idea"), key=lambda n: n["id"])
    selected = [n for n in ideas if len(n["essays"]) >= MIN_ESSAYS]
    return selected, [n for n in ideas if len(n["essays"]) < MIN_ESSAYS]


def merge_blocks(labels: list[str]) -> list[list[str]]:
    labels = sorted(labels)
    if len(labels) <= ONE_CALL_MAX:
        return [labels]
    by_letter = defaultdict(list)
    for label in labels:
        by_letter[label.casefold()[:1]].append(label)
    return [g[i:i + MAX_BLOCK] for _, g in sorted(by_letter.items()) for i in range(0, len(g), MAX_BLOCK)]


# --- prompts and parsing ---


def merge_prompt(nodes: list[dict]) -> str:
    lines = ["Ideas (label | other spellings | essays | one description per essay):"]
    for n in sorted(nodes, key=lambda n: n["label"]):
        descs = " / ".join(n["descriptions"].values())
        lines.append(f"- {n['label']} | {', '.join(n['aliases']) or '-'} | {len(n['essays'])} | {descs}")
    return "\n".join(lines)


def themes_prompt(ideas: list[tuple[str, str]]) -> str:
    return "\n".join(["Ideas (label | description):"] + [f"- {label} | {desc}" for label, desc in sorted(ideas)])


def parse_clusters(text: str, labels: list[str]) -> tuple[list[list[str]], int]:
    """Same rules as task 04: a cluster with an unknown or reused label is rejected whole."""
    return mn.parse_clusters(text, labels)


def parse_themes(text: str, labels: list[str]) -> tuple[dict[str, str], dict]:
    """label -> theme name. Unknown labels are dropped, a repeated label keeps its first theme,
    a missing label goes to OTHER_THEME; each is counted."""
    try:
        out = ThemesOut.model_validate_json(text)
    except ValidationError as exc:
        raise BadJsonError(str(exc).splitlines()[0]) from exc
    allowed = set(labels)
    themes, stats = {}, {"unknown": 0, "duplicate": 0, "missing": 0}
    for t in out.themes:
        name = t.name.strip() or OTHER_THEME
        for label in t.ideas:
            if label not in allowed:
                stats["unknown"] += 1
            elif label in themes:
                stats["duplicate"] += 1
            else:
                themes[label] = name
    for label in sorted(allowed - set(themes)):
        themes[label] = OTHER_THEME
        stats["missing"] += 1
    return {label: themes[label] for label in labels}, stats


# --- model calls (cached) ---


def cached_call(kind: str, system: str, prompt: str, out_dir: Path, force: bool, offline: bool) -> tuple[str | None, str]:
    """(response text, status). status is ok or no_raw. Raises extract.CliError."""
    digest = hashlib.sha1(f"{system}\n{prompt}".encode("utf-8")).hexdigest()[:12]
    raw_path = out_dir / "raw" / f"{kind}_{digest}.json"
    if raw_path.exists() and not force:
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
    elif offline:
        return None, "no_raw"
    else:
        raw = extract.run_claude_cli(extract.MODELS["sonnet"], system, prompt)
        raw["prompt"] = prompt
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
    return extract.response_text(raw), "ok"


# --- labels and overrides ---


def canonical(members: list[dict]) -> dict:
    """The member whose label is used in the most essays; tie goes to the longer label."""
    return max(members, key=lambda n: (len(n["essays"]), len(n["label"]), n["label"]))


def merged_label(members: list[dict], override: str | None = None) -> tuple[str, list[str]]:
    label = override or canonical(members)["label"]
    forms = {f for n in members for f in [n["label"], *n["aliases"]]}
    return label, sorted(forms - {label})


def apply_merge_overrides(groups: list[list[str]], nodes_by_label: dict[str, dict], overrides: dict):
    """(groups of node ids, {canonical id: label override}, warnings). Reuses task 04's override rules."""
    id_of = {label: n["id"] for label, n in nodes_by_label.items()}
    by_id = {n["id"]: n for n in nodes_by_label.values()}
    clusters = [mn.Cluster("idea", [by_id[i]["label"] for i in g]) for g in groups]
    ov = {k: overrides.get(k, default) for k, default in (("merge", []), ("keep_apart", []), ("label", {}))}
    clusters, warnings = mn.apply_overrides(clusters, ov)
    out, labels = [], {}
    for c in clusters:
        ids = sorted(id_of[m] for m in c.members)
        out.append(ids)
        if c.label_override:
            labels[canonical([by_id[i] for i in ids])["id"]] = c.label_override
    return out, labels, warnings


def apply_theme_overrides(themes: dict[str, str], overrides: dict, forms: dict[str, list[str]]):
    """themes: merged label -> theme. forms: merged label -> every label/alias it covers."""
    themes, warnings = dict(themes), []
    for name, theme in overrides.get("theme", {}).items():
        hit = next((label for label, fs in forms.items() if name.casefold() in {f.casefold() for f in [label, *fs]}),
                   None)
        if hit is None:
            warnings.append(f"theme: unknown idea {name!r}")
        else:
            themes[hit] = theme
    return themes, warnings


# --- graph ---


def _para_key(p: str):
    return int(p[1:]) if p[1:].isdigit() else 0


def build_grouped(graph: dict, groups: list[list[str]], themes: dict[str, str],
                  labels: dict[str, str] | None = None) -> tuple[dict, dict]:
    """Merge each group of idea ids into one node with a theme. Ideas in no group pass through unchanged.
    themes: merged label -> theme name (missing: OTHER_THEME). labels: any member id -> label override."""
    labels = labels or {}
    by_id = {n["id"]: n for n in graph["nodes"]}
    id_map, merged = {}, {}
    for g in groups:
        members = sorted((by_id[i] for i in g), key=lambda n: n["id"])
        head = canonical(members)
        members = [head] + [n for n in members if n is not head]
        override = next((labels[n["id"]] for n in members if n["id"] in labels), None)
        label, aliases = merged_label(members, override)
        descriptions = {}
        for n in members:
            for eid, d in n["descriptions"].items():
                descriptions.setdefault(eid, d)
            id_map[n["id"]] = head["id"]
        merged[head["id"]] = {**head, "label": label, "aliases": aliases,
                              "descriptions": dict(sorted(descriptions.items())),
                              "essays": sorted({e for n in members for e in n["essays"]}),
                              "mention_count": sum(n["mention_count"] for n in members),
                              "theme": themes.get(label, OTHER_THEME)}

    nodes = [merged.get(n["id"], n) for n in graph["nodes"] if id_map.get(n["id"], n["id"]) == n["id"]]
    theme_ids = {}
    for t in sorted({n["theme"] for n in merged.values()}):
        theme_ids[t] = f"theme:{mn.slug(t)}"
        nodes.append({"id": theme_ids[t], "label": t, "type": "theme"})

    links, mention_at, stats = [], {}, {"self_loops": 0, "folded_mentions": 0}
    for link in graph["links"]:
        s, t = id_map.get(link["source"], link["source"]), id_map.get(link["target"], link["target"])
        if s == t:
            stats["self_loops"] += 1
            continue
        link = {**link, "source": s, "target": t}
        if link["kind"] == "mentioned_in":
            key = (s, t)
            if key in mention_at:
                kept = links[mention_at[key]]
                kept["paragraphs"] = sorted(set(kept["paragraphs"]) | set(link["paragraphs"]), key=_para_key)
                stats["folded_mentions"] += 1
                continue
            mention_at[key] = len(links)
        links.append(link)
    for node_id in sorted(merged):
        links.append({"source": node_id, "target": theme_ids[merged[node_id]["theme"]], "kind": "in_theme"})
    stats["in_theme"] = len(merged)
    nodes.sort(key=lambda n: n["id"])
    return {"nodes": nodes, "links": links}, stats


# --- summary ---


def render_summary(selected, rest, groups, merged_nodes, themes, run, gstats, graph_in, graph_out, warnings) -> str:
    multi = [n for n in merged_nodes if n["_members"] > 1]
    by_theme = defaultdict(list)
    for n in merged_nodes:
        by_theme[n["theme"]].append(n["label"])
    out = ["# ideas summary", "", "## counts", "",
           f"- ideas in graph.json: {len(selected) + len(rest)} ({len(selected)} in {MIN_ESSAYS}+ essays, "
           f"{len(rest)} pass through with no theme)",
           f"- selected ideas after merging: {len(merged_nodes)} ({len(selected) - len(merged_nodes)} merged away, "
           f"{len(multi)} merged nodes)",
           f"- themes: {len(by_theme)}",
           f"- merge calls: {run['merge_calls']}, rejected clusters: {run['rejected_clusters']}, "
           f"bad_json: {run['merge_bad_json']}, no_raw: {run['merge_no_raw']}",
           f"- themes call: {run['themes_status']}; rejected: unknown {run['themes']['unknown']}, "
           f"duplicate {run['themes']['duplicate']}, missing {run['themes']['missing']}",
           f"- links: {len(graph_in['links'])} in − {gstats['self_loops']} self-loops − "
           f"{gstats['folded_mentions']} folded mentioned_in + {gstats['in_theme']} in_theme = {len(graph_out['links'])}",
           f"- nodes: {len(graph_in['nodes'])} in → {len(graph_out['nodes'])} out", ""]
    out += ["## override warnings", ""] + ([f"- {w}" for w in warnings] or ["none"]) + [""]
    sample = sorted(random.Random(SAMPLE_SEED).sample(multi, min(SAMPLE_SIZE, len(multi))), key=lambda n: n["id"])
    out += [f"## {len(sample)} random merges to check (seed {SAMPLE_SEED})", ""] + [_merge_line(n) for n in sample] + [""]
    out += [f"## all merges ({len(multi)})", "", "one line per node: label ← labels merged into it — descriptions", ""]
    out += [_merge_line(n) for n in multi] + [""]
    out += ["## themes", ""]
    for t in sorted(by_theme):
        out.append(f"- **{t}** ({len(by_theme[t])}): {', '.join(sorted(by_theme[t], key=str.casefold))}")
    return "\n".join(out) + "\n"


def _merge_line(n: dict) -> str:
    descs = list(n["descriptions"].values())[:2]
    return f"- {n['label']} [{n['theme']}] ← {', '.join(n['_member_labels'])} — " + " / ".join(descs)


# --- running ---


def main():
    parser = argparse.ArgumentParser(description="Merge and theme ideas into extract/graph_grouped.json")
    parser.add_argument("--extract-dir", type=Path, default=extract.DEFAULT_OUT_DIR)
    parser.add_argument("--overrides", type=Path, default=OVERRIDES_FILE)
    parser.add_argument("--force", action="store_true", help="call the model even when cached")
    parser.add_argument("--offline", action="store_true", help="use cached answers only; never call the model")
    args = parser.parse_args()
    force = args.force and not args.offline

    out_dir = args.extract_dir / "ideas"
    out_dir.mkdir(parents=True, exist_ok=True)
    graph = json.loads((args.extract_dir / "graph.json").read_text(encoding="utf-8"))
    selected, rest = select_ideas(graph)
    nodes_by_label = {n["label"]: n for n in selected}
    (out_dir / "candidates.json").write_text(json.dumps(
        [{k: n[k] for k in ("id", "label", "aliases", "essays", "descriptions")} for n in selected],
        ensure_ascii=False, indent=1), encoding="utf-8")

    run = {"merge_calls": 0, "rejected_clusters": 0, "merge_bad_json": 0, "merge_no_raw": 0}
    label_groups = []
    try:
        for block in merge_blocks(list(nodes_by_label)):
            run["merge_calls"] += 1
            text, status = cached_call("merge", MERGE_SYSTEM, merge_prompt([nodes_by_label[l] for l in block]),
                                       out_dir, force, args.offline)
            clusters = [[l] for l in block]
            if status == "no_raw":
                run["merge_no_raw"] += 1
            else:
                try:
                    clusters, rejected = parse_clusters(text, block)
                    run["rejected_clusters"] += rejected
                except BadJsonError:
                    run["merge_bad_json"] += 1
            label_groups += clusters
    except extract.CliError as exc:
        sys.exit(f"cli_error in merge call: {exc}; rerun later to resume. graph_grouped.json not written.")

    groups = [[nodes_by_label[l]["id"] for l in c] for c in label_groups]
    overrides = json.loads(args.overrides.read_text(encoding="utf-8")) if args.overrides.exists() else {}
    groups, label_ov, warnings = apply_merge_overrides(groups, nodes_by_label, overrides)
    by_id = {n["id"]: n for n in selected}
    merged = []  # (label, aliases, first description, member nodes)
    for g in sorted(groups):
        members = [by_id[i] for i in g]
        label, aliases = merged_label(members, label_ov.get(canonical(members)["id"]))
        merged.append((label, aliases, next(iter(canonical(members)["descriptions"].values()), ""), members))

    labels = [m[0] for m in merged]
    try:
        text, status = cached_call("themes", THEMES_SYSTEM, themes_prompt([(m[0], m[2]) for m in merged]),
                                   out_dir, force, args.offline)
    except extract.CliError as exc:
        sys.exit(f"cli_error in themes call: {exc}; rerun later to resume. graph_grouped.json not written.")
    run["themes"] = {"unknown": 0, "duplicate": 0, "missing": 0}
    themes = {label: OTHER_THEME for label in labels}
    run["themes_status"] = status
    if status == "ok":
        try:
            themes, run["themes"] = parse_themes(text, labels)
        except BadJsonError:
            run["themes_status"] = "bad_json"
    themes, theme_warnings = apply_theme_overrides(themes, overrides, {m[0]: m[1] for m in merged})
    warnings += theme_warnings
    for w in warnings:
        print(f"override warning: {w}", file=sys.stderr)

    out, gstats = build_grouped(graph, groups, themes, label_ov)
    (args.extract_dir / "graph_grouped.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "clusters.json").write_text(json.dumps(
        [{"label": m[0], "members": sorted(n["label"] for n in m[3])} for m in merged if len(m[3]) > 1],
        ensure_ascii=False, indent=1), encoding="utf-8")
    by_theme = defaultdict(list)
    for label in labels:
        by_theme[themes[label]].append(label)
    (out_dir / "themes.json").write_text(json.dumps(
        [{"name": t, "ideas": sorted(by_theme[t])} for t in sorted(by_theme)], ensure_ascii=False, indent=1),
        encoding="utf-8")

    out_by_id = {n["id"]: n for n in out["nodes"]}
    merged_nodes = []
    for m in merged:
        n = dict(out_by_id[canonical(m[3])["id"]])
        n["_members"], n["_member_labels"] = len(m[3]), sorted(x["label"] for x in m[3])
        merged_nodes.append(n)
    (out_dir / "ideas_summary.md").write_text(
        render_summary(selected, rest, groups, merged_nodes, themes, run, gstats, graph, out, warnings),
        encoding="utf-8")
    types = Counter(n["type"] for n in out["nodes"])
    print(f"graph_grouped.json: {len(out['nodes'])} nodes ({dict(types)}), {len(out['links'])} links; "
          f"ideas {len(selected)} → {len(merged)}, themes {len(by_theme)}, self-loops {gstats['self_loops']}, "
          f"folded {gstats['folded_mentions']}, merge {run['merge_calls']} call(s), themes {run['themes_status']}")


if __name__ == "__main__":
    main()
