#!/usr/bin/env python3
"""
Corpus summary for the full extraction run: extract/corpus_summary.md.

Every number is rebuilt from the saved raw answers (extract/raw/<model>/), so the
summary matches what is on disk, whatever runs and retries happened before.
extract/last_run.json (written by extract.py) tells a cli_error from an essay
that was never started; without it, both count as "no answer".

Usage:
    python3 corpus_summary.py            # sonnet, writes extract/corpus_summary.md
"""

import argparse
import json
import random
from collections import Counter
from pathlib import Path

import extract

SEED = 20261111
SAMPLE_SIZE = 5
THRESHOLDS = {"drop_share": 0.05, "associated_share": 0.30}


def collect(data_dir: Path, out_dir: Path, alias: str = "sonnet") -> dict:
    last_run = {}
    if (out_dir / "last_run.json").exists():
        for stem, _alias, status in json.loads((out_dir / "last_run.json").read_text())["failures"]:
            last_run[stem] = status

    done, bad_json, cli_error, not_started = [], [], [], []
    for md_path in extract.select_paths(data_dir, "all"):
        essay = extract.parse_essay(md_path.read_text(encoding="utf-8"))
        raw_path = out_dir / "raw" / alias / f"{essay['id']}.json"
        if not raw_path.exists():
            (cli_error if last_run.get(essay["id"]) == "cli_error" else not_started).append(essay["id"])
            continue
        try:
            done.append(extract.build_result(essay, alias, json.loads(raw_path.read_text(encoding="utf-8"))))
        except extract.BadJson:
            bad_json.append(essay["id"])

    entities = Counter({t: 0 for t in extract.ENTITY_TYPES})
    kinds = Counter({k: 0 for k in extract.RELATION_KINDS})
    drops = Counter()
    unlinked = Counter()
    rows = []
    for r in done:
        entities.update(e["type"] for e in r["entities"])
        kinds.update(x["kind"] for x in r["relations"])
        rel_drops = [d for d in r["dropped"] if "source" in d["item"]]  # entity-level drops aren't links
        drops.update(d["reason"] for d in rel_drops)
        base = {e["name"]: e.get("base_name") or e["name"] for e in r["entities"]}
        unlinked.update(base[name] for name in r["unlinked"])
        proposed = len(r["relations"]) + len(rel_drops)
        rows.append({
            "id": r["essay"]["id"],
            "number": r["essay"]["number"],
            "entities": len(r["entities"]),
            "links": len(r["relations"]),
            "drops": len(rel_drops),
            "proposed": proposed,
            "drop_rate": len(rel_drops) / proposed if proposed else 0.0,
            "associated": sum(1 for x in r["relations"] if x["kind"] == "associated_with"),
            "unlinked": len(r["unlinked"]),
            "duration_ms": r.get("duration_ms"),
        })

    links = sum(kinds.values())
    proposed = links + sum(drops.values())
    candidates = sorted(row["id"] for row in rows if row["number"] not in extract.PILOT_ESSAYS)
    sample = sorted(random.Random(SEED).sample(candidates, min(SAMPLE_SIZE, len(candidates))))

    return {
        "alias": alias,
        "done": [row["id"] for row in rows],
        "bad_json": bad_json,
        "cli_error": cli_error,
        "not_started": not_started,
        "rows": rows,
        "totals": {
            "entities": dict(entities),
            "kinds": dict(kinds),
            "links": links,
            "proposed": proposed,
            "drops_by_reason": dict(drops),
            "drop_share": sum(drops.values()) / proposed if proposed else 0.0,
            "associated_share": kinds["associated_with"] / links if links else 0.0,
            "unlinked": sum(unlinked.values()),
            "run_time_ms": sum(row["duration_ms"] or 0 for row in rows),
        },
        "unlinked_top": unlinked.most_common(20),
        "sample": sample,
    }


def _pct(x: float) -> str:
    return f"{100 * x:.1f}%"


def _verdict(ok: bool) -> str:
    return "PASS" if ok else "FAIL"


def render(s: dict) -> str:
    t = s["totals"]
    alias = s["alias"]
    total = len(s["done"]) + len(s["bad_json"]) + len(s["cli_error"]) + len(s["not_started"])
    out = [f"# corpus summary: extraction on {alias}", ""]

    out += ["## status", "",
            f"- essays: {total}",
            f"- done: {len(s['done'])}",
            f"- bad_json: {len(s['bad_json'])}" + (f" ({', '.join(s['bad_json'])})" if s["bad_json"] else ""),
            f"- cli_error: {len(s['cli_error'])}" + (f" ({', '.join(s['cli_error'])})" if s["cli_error"] else ""),
            f"- not started: {len(s['not_started'])}"
            + (f" ({', '.join(s['not_started'])})" if s["not_started"] else ""),
            ""]
    out += [f"bad_json: {x}" for x in s["bad_json"]] + [f"cli_error: {x}" for x in s["cli_error"]]
    if s["bad_json"] or s["cli_error"]:
        out.append("")

    out += ["## totals", "",
            "- entities: " + ", ".join(f"{k} {v}" for k, v in t["entities"].items())
            + f" ({sum(t['entities'].values())})",
            "- links: " + ", ".join(f"{k} {v}" for k, v in t["kinds"].items()) + f" ({t['links']})",
            f"- share of associated_with: {_pct(t['associated_share'])}",
            "- drops: " + (", ".join(f"{k} {v}" for k, v in sorted(t["drops_by_reason"].items())) or "none")
            + f" ({sum(t['drops_by_reason'].values())} of {t['proposed']} proposed links, {_pct(t['drop_share'])})",
            f"- unlinked person/work: {t['unlinked']}",
            f"- model time, summed: {t['run_time_ms'] / 60000:.1f} min",
            ""]

    out += ["## thresholds", "",
            "| threshold | value | result |", "|---|---|---|",
            f"| drops < 5% of proposed links | {_pct(t['drop_share'])} "
            f"| {_verdict(t['drop_share'] < THRESHOLDS['drop_share'])} |",
            f"| 0 bad_json after the retry | {len(s['bad_json'])} | {_verdict(not s['bad_json'])} |",
            f"| associated_with < 30% of links | {_pct(t['associated_share'])} "
            f"| {_verdict(t['associated_share'] < THRESHOLDS['associated_share'])} |",
            "", "a FAIL doesn't block anything; it's a signal for plan and the user.", ""]

    out += ["## 5 random essays to read", "",
            f"seed {SEED}, chosen from the done essays without the pilot ones ({', '.join(map(str, extract.PILOT_ESSAYS))}).", ""]
    out += [f"- [{x}]({alias}/{x}.review.md)" for x in s["sample"]] + [""]

    def table(rows):
        lines = ["| essay | entities | links | drops | unlinked | run time |", "|---|---|---|---|---|---|"]
        for row in rows:
            secs = f"{row['duration_ms'] / 1000:.1f} s" if row["duration_ms"] is not None else "–"
            lines.append(f"| {row['id']} | {row['entities']} | {row['links']} | {row['drops']} "
                         f"| {row['unlinked']} | {secs} |")
        return lines

    worst_drops = sorted((r for r in s["rows"] if r["drops"]), key=lambda r: (-r["drop_rate"], -r["drops"], r["id"]))[:10]
    out += ["## highest drop rate", "", "| essay | drops | proposed | rate |", "|---|---|---|---|"]
    out += [f"| {r['id']} | {r['drops']} | {r['proposed']} | {_pct(r['drop_rate'])} |" for r in worst_drops] or ["none"]
    out.append("")

    most_assoc = sorted((r for r in s["rows"] if r["associated"]), key=lambda r: (-r["associated"], r["id"]))[:10]
    out += ["## most associated_with", "", "| essay | associated_with | links |", "|---|---|---|"]
    out += [f"| {r['id']} | {r['associated']} | {r['links']} |" for r in most_assoc] or ["none"]
    out.append("")

    out += ["## unlinked person/work", "", f"{t['unlinked']} in total; the 20 most common, by base_name:", ""]
    out += [f"- {name}: {n}" for name, n in s["unlinked_top"]] or ["none"]
    out.append("")

    out += ["## per essay", ""] + table(s["rows"])
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Summarise the full extraction run")
    parser.add_argument("--model", choices=list(extract.MODELS), default="sonnet")
    parser.add_argument("--data-dir", type=Path, default=extract.DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=extract.DEFAULT_OUT_DIR)
    args = parser.parse_args()
    summary = collect(args.data_dir, args.out_dir, args.model)
    path = args.out_dir / "corpus_summary.md"
    path.write_text(render(summary), encoding="utf-8")
    print(f"{path}: {len(summary['done'])} done, {len(summary['bad_json'])} bad_json, "
          f"{len(summary['cli_error'])} cli_error, {len(summary['not_started'])} not started")


if __name__ == "__main__":
    main()
