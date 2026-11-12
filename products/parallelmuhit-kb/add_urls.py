"""Task 07: carry the urls of essay links into the extraction output and the graph. Offline, no model calls.

1. every extract/sonnet/*.json paragraph gets `links` ([{text, url}]), re-parsed from essays_md and matched
   by global_id (a paragraph text that no longer matches stops the run).
2. graph.json and graph_grouped.json get `urls` on
   - relation links: the paragraph's links whose anchor text occurs inside the quote,
   - mentioned_in links: every link of their paragraphs,
   - nodes: links whose anchor equals the node's label or an alias (casefolded, apostrophes dropped).
   `urls` is omitted when empty. A rerun gives the same bytes.

    python add_urls.py            # patches the files in place and prints how many urls were left out
"""

import argparse
import json
import sys
from pathlib import Path

import extract
import merge_names as mn
from export_markdown import DEFAULT_DATA_DIR

HERE = Path(__file__).parent
EXTRACT_DIR = HERE / "extract"
GRAPHS = ("graph.json", "graph_grouped.json")


def _fold(s: str) -> str:
    s = s.casefold()
    for ch in mn._APOSTROPHES:
        s = s.replace(ch, "")
    return " ".join(s.split())


def patch_paragraphs(result: dict, md: str) -> int:
    """Add `links` to every paragraph of one extraction result. Returns the number of links added."""
    essay = extract.parse_essay(md)
    by_id = {p["id"]: p for p in essay["paragraphs"]}
    total = 0
    for p in result["paragraphs"]:
        fresh = by_id.get(p["id"])
        if fresh is None or fresh["text"] != p["text"]:
            raise ValueError(f"paragraph {p['global_id']} no longer matches the markdown")
        p["links"] = fresh["links"]
        total += len(fresh["links"])
    return total


def _dedupe(links: list[dict]) -> list[dict]:
    seen, out = set(), []
    for l in links:
        if l["url"] not in seen:
            seen.add(l["url"])
            out.append({"text": l["text"], "url": l["url"]})
    return out


def attach_urls(graph: dict, results: list[dict]) -> tuple[dict, dict]:
    """Return a copy of the graph with `urls`, and counts of the urls attached / left out."""
    para = {}  # (essay, local id) -> links
    for r in results:
        eid = r["essay"]["id"]
        for p in r["paragraphs"]:
            para[(eid, p["id"])] = p.get("links", [])

    nodes = [{k: v for k, v in n.items() if k != "urls"} for n in graph["nodes"]]
    links = [{k: v for k, v in l.items() if k != "urls"} for l in graph["links"]]
    attached = set()  # (essay, url) reaching the graph

    for l in links:
        eid = l.get("essay")
        if l["kind"] == "mentioned_in":
            found = [u for pid in l["paragraphs"] for u in para.get((eid, pid), [])]
        elif l.get("paragraph") and l.get("quote"):
            quote = " ".join(l["quote"].split())
            found = [u for u in para.get((eid, l["paragraph"]), []) if " ".join(u["text"].split()) in quote]
        else:
            continue
        found = _dedupe(found)
        if found:
            l["urls"] = found
            attached.update((eid, u["url"]) for u in found)

    names = {}  # folded name -> node
    for n in nodes:
        if n["type"] in ("essay", "author", "theme"):
            continue
        for s in [n["label"], *n.get("aliases", [])]:
            names.setdefault(_fold(s), []).append(n)
    node_urls = {}
    for r in results:
        eid = r["essay"]["id"]
        for p in r["paragraphs"]:
            for u in p.get("links", []):
                for n in names.get(_fold(u["text"]), []):
                    node_urls.setdefault(n["id"], []).append(u)
                    attached.add((eid, u["url"]))
    for n in nodes:
        if n["id"] in node_urls:
            n["urls"] = _dedupe(node_urls[n["id"]])

    total = {(r["essay"]["id"], u["url"]) for r in results for p in r["paragraphs"] for u in p.get("links", [])}
    stats = {"urls_total": len(total), "urls_attached": len(total & attached),
             "urls_left_out": len(total - attached)}
    return {"nodes": nodes, "links": links}, stats


def _dump(obj, indent: int) -> str:  # same format the pipeline writes (no trailing newline)
    return json.dumps(obj, ensure_ascii=False, indent=indent)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    ap.add_argument("--extract-dir", type=Path, default=EXTRACT_DIR)
    args = ap.parse_args()

    sonnet = sorted((args.extract_dir / "sonnet").glob("*.json"))
    results, occurrences = [], 0
    for f in sonnet:
        r = json.loads(f.read_text(encoding="utf-8"))
        md = (args.data_dir / "essays_md" / f"{r['essay']['number']:03d}_{r['essay']['slug']}.md").read_text(encoding="utf-8")
        occurrences += patch_paragraphs(r, md)
        f.write_text(_dump(r, 2), encoding="utf-8")
        results.append(r)
    print(f"{len(results)} essays, {occurrences} link occurrences (http/https, deduped per paragraph)")

    for name in GRAPHS:
        path = args.extract_dir / name
        graph, stats = attach_urls(json.loads(path.read_text(encoding="utf-8")), results)
        path.write_text(_dump(graph, 1), encoding="utf-8")
        print(f"{name}: {stats}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
