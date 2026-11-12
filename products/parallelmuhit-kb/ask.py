"""ask.py "savol": answer an Uzbek question from the essays, with citations checked by code (task 08).

retrieve.py picks the context, sonnet answers via `claude -p`, and every cited paragraph id is verified
against the context. Quotes and urls shown to the user are copied from the data, never from the model.
"""

import argparse
import re
import sys
from pathlib import Path

import retrieve

HERE = Path(__file__).parent
NOT_FOUND = "essalarda bu haqda topilmadi"
QUOTE_MAX = 400

SYSTEM = f"""Sen Aziz Rahimovning parallelmuhit.uz esselari bo'yicha savollarga javob berasan.
Qoidalar:
- Faqat berilgan kontekstdan foydalan. O'zingdan hech narsa qo'shma.
- O'zbek tilida, qisqa va aniq javob ber.
- Har bir da'vodan keyin manbani shu ko'rinishda yoz: [003_javoblar#p13]. Faqat kontekstdagi id'lardan foydalan.
- Kontekst savolga javob bermasa, aynan shunday yoz: "{NOT_FOUND}"."""

BRACKET = re.compile(r"\[([^\[\]]*#p\d+[^\[\]]*)\]")
ID = re.compile(r"[\w]+#p\d+")


def build_prompt(question: str, ctx: dict) -> str:
    out = ["PARAGRAFLAR:"]
    out += [f"[{p['id']}] ({p['title']}) {p['text']}" for p in ctx["paragraphs"]]
    if ctx["links"]:
        out.append("\nMUNOSABATLAR (graf):")
        out += [f"- {l['source']} —{l['kind']}→ {l['target']}: \"{l['quote']}\" [{l['paragraph_id']}]" for l in ctx["links"]]
    out.append(f"\nSAVOL: {question}")
    return "\n".join(out)


def verify(answer: str, allowed: set[str]) -> tuple[str, list[str], list[str]]:
    """-> (answer without fake ids, valid ids in order of first appearance, dropped ids)."""
    valid: list[str] = []
    dropped: list[str] = []

    def fix(m: re.Match) -> str:
        keep = []
        for i in ID.findall(m.group(1)):
            if i in allowed:
                keep.append(i)
                if i not in valid:
                    valid.append(i)
            elif i not in dropped:
                dropped.append(i)
        return f"[{', '.join(keep)}]" if keep else ""

    return BRACKET.sub(fix, answer), valid, dropped


def citation(pid: str, corpus: dict, ctx: dict) -> dict:
    p = corpus[pid]
    link = next((l for l in ctx["links"] if l["paragraph_id"] == pid), None)
    return {"id": pid, "title": p["title"], "url": p["source"], "links": p["links"],
            "quote": link["quote"] if link else p["text"][:QUOTE_MAX]}


def ask(question: str, corpus: dict, bm25: retrieve.BM25, nodes: list[dict], links: list[dict], generate) -> dict:
    ctx = retrieve.retrieve(question, corpus, bm25, nodes, links)
    raw = generate(SYSTEM, build_prompt(question, ctx))
    answer, valid, dropped = verify(raw, retrieve.allowed_ids(ctx))
    not_found = NOT_FOUND in retrieve.fold(answer)
    return {"question": question, "answer": answer, "dropped": dropped,
            "citations": [citation(i, corpus, ctx) for i in valid],
            "flagged": bool(dropped) or (not valid and not not_found)}


def render(r: dict) -> str:
    out = [r["answer"].strip(), ""]
    for c in r["citations"]:
        out.append(f"[{c['id']}] {c['title']}\n  «{c['quote']}»\n  {c['url']}")
        out += [f"  ↗ {l['text']}: {l['url']}" for l in c["links"]]
    if r["flagged"]:
        why = f"yo'q manbalar olib tashlandi: {', '.join(r['dropped'])}" if r["dropped"] else "javobda tekshirilgan manba yo'q"
        out.append(f"\nOGOHLANTIRISH: {why}. Javobga ishonmang.")
    return "\n".join(out)


def cli_generate(system: str, prompt: str) -> str:
    import extract
    raw = extract.run_claude_cli(extract.MODELS["sonnet"], system, prompt)
    return raw["content"][0]["text"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("question")
    ap.add_argument("--context", action="store_true", help="print the retrieved context only, no model call")
    ap.add_argument("--graph", type=Path, default=HERE / "extract" / "graph_grouped.json")
    ap.add_argument("--sonnet-dir", type=Path, default=HERE / "extract" / "sonnet")
    a = ap.parse_args(argv)

    import json
    g = json.loads(a.graph.read_text(encoding="utf-8"))
    corpus = retrieve.load_corpus(a.sonnet_dir)
    bm25 = retrieve.BM25(list(corpus.values()))
    if a.context:
        ctx = retrieve.retrieve(a.question, corpus, bm25, g["nodes"], g["links"])
        print(build_prompt(a.question, ctx))
        return 0
    print(render(ask(a.question, corpus, bm25, g["nodes"], g["links"], cli_generate)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
