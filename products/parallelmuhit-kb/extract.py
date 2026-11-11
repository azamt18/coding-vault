#!/usr/bin/env python3
"""
Extraction pilot: pull entities and quote-backed relations out of essays with Claude.

One call per essay per model. The model sees the title and numbered plain-text
paragraphs; code checks every relation against the essay and drops (never fixes)
what doesn't hold. Code also builds the essay node, the author node and the
mentioned_in edges.

Usage:
    python3 extract.py                                  # pilot essays 2,149,180 on both models
    python3 extract.py --essays 149 --model haiku
    python3 extract.py --force                          # ignore cached raw responses

The key comes from ANTHROPIC_API_KEY only. Outputs go to extract/ next to this
script (gitignored): raw/<model>/NNN_slug.json, <model>/NNN_slug.json,
<model>/NNN_slug.review.md and compare.md.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from export_markdown import AUTHOR, DEFAULT_DATA_DIR

HERE = Path(__file__).resolve().parent
DEFAULT_OUT_DIR = HERE / "extract"
PILOT_ESSAYS = [2, 149, 180]

MODELS = {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5"}
# USD per 1M tokens (input, output), from the claude-api skill's model table (cached 2026-10-06).
# haiku 5.5's rate is for prompts up to 100K tokens; a whole essay is far below that.
PRICES = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.00, 10.00)}
EFFORT = "high"
MAX_TOKENS = 16000

ENTITY_TYPES = ["person", "work", "idea", "organization"]
RELATION_KINDS = ["wrote", "recommends", "criticises", "inspired_by", "example_of", "associated_with"]


# --- response schema (type/kind stay plain strings so code, not the decoder, enforces the lists) ---


class Entity(BaseModel):
    name: str = Field(description="exactly as written in the essay")
    type: str = Field(description="one of: " + ", ".join(ENTITY_TYPES))
    description: str = Field(description="one sentence in Uzbek, grounded in the essay")
    aliases: list[str] = Field(description="other spellings of this entity in this essay")
    paragraphs: list[str] = Field(description="paragraph ids where it appears, e.g. p3")


class Relation(BaseModel):
    source: str
    target: str
    kind: str = Field(description="one of: " + ", ".join(RELATION_KINDS))
    label: str = Field(description="short phrase in Uzbek, the essay's own wording")
    paragraph: str = Field(description="the paragraph id the quote comes from")
    quote: str = Field(description="exact text copied from that paragraph")


class Extraction(BaseModel):
    entities: list[Entity]
    relations: list[Relation]


# --- essay → paragraphs ---

_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_RULE = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
_DATE = re.compile(r"^\d{1,2}\.\d{1,2}\.\d{4}$")


def plain_text(block: str) -> str:
    """Markdown block → the text the model sees and quotes are checked against.

    Removes images, link syntax (keeps the text), heading marks, `>` and `*`/`_`
    emphasis. Apostrophes and Uzbek letters are left byte for byte.
    """
    lines = []
    for line in block.splitlines():
        line = re.sub(r"^\s*(>\s?)+", "", line)
        line = re.sub(r"^\s*#{1,6}\s+", "", line)
        lines.append(line)
    text = " ".join(lines)
    text = _IMAGE.sub("", text)
    text = _LINK.sub(r"\1", text)
    text = text.replace("*", "")
    text = re.sub(r"(?<![\w])_+|_+(?![\w])", "", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def parse_essay(md: str) -> dict:
    if not md.startswith("---\n"):
        raise ValueError("essay has no frontmatter")
    _, head, body = md.split("---\n", 2)  # only the first two rules; the body may have its own
    meta = yaml.safe_load(head)
    essay_id = f"{meta['number']:03d}_{meta['slug']}"

    paragraphs = []
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if not block or _RULE.match(block):
            continue
        text = plain_text(block)
        if not text or _DATE.match(text):  # image-only blocks end up empty
            continue
        paragraphs.append({"id": f"p{len(paragraphs) + 1}", "text": text})
    return {"id": essay_id, "meta": meta, "paragraphs": paragraphs}


# --- prompt ---

SYSTEM = f"""\
You extract a knowledge graph from one Uzbek essay. All essays are written by {AUTHOR}.
When the essay says "men", "biz" or otherwise speaks in the author's own voice, that is {AUTHOR}.

Return entities and relations.

Entities: only what the essay actually discusses, not every passing word.
- name: exactly as written in the essay, including its apostrophes and letters.
- type: one of {", ".join(ENTITY_TYPES)}.
  work = book, article, film, podcast or talk. Do not extract places or events.
- description: one sentence in Uzbek, based only on what the essay says.
- aliases: other spellings of the same entity in this essay (may be empty).
- paragraphs: ids of the paragraphs where it appears.
Do not list {AUTHOR} as an entity; refer to him by that name in relations.

Relations: source --kind--> target, for example person wrote work, idea example_of idea.
- source and target: entity names from your list, or "{AUTHOR}".
- kind: one of {", ".join(RELATION_KINDS)}.
- label: a short phrase in Uzbek, using the essay's own wording.
- paragraph: the id of the paragraph that supports it.
- quote: text copied exactly, character for character, from that paragraph. Do not change
  apostrophes (ʻ ‘ ’ ') or letters, and do not join text from different paragraphs.
Only include relations the essay states or clearly argues.
"""


def build_prompt(essay: dict) -> str:
    lines = [f"Title: {essay['meta']['title']}", "", "Paragraphs:"]
    lines += [f"[{p['id']}] {p['text']}" for p in essay["paragraphs"]]
    return "\n".join(lines)


# --- checks ---


def check_quote(essay: dict, paragraph_id: str, quote: str) -> str | None:
    """None if the quote is an exact substring of that paragraph, else the drop reason."""
    para = next((p for p in essay["paragraphs"] if p["id"] == paragraph_id), None)
    if para is None:
        return "bad_paragraph"
    if not quote or quote not in para["text"]:
        return "quote_not_found"
    return None


def response_text(raw: dict) -> str:
    for block in raw.get("content", []):
        if block.get("type") == "text":
            return block["text"]
    raise ValueError(f"no text block in response (stop_reason={raw.get('stop_reason')})")


def cost_usd(model_id: str, usage: dict) -> float:
    price_in, price_out = PRICES[model_id]
    return usage["input_tokens"] * price_in / 1e6 + usage["output_tokens"] * price_out / 1e6


def build_result(essay: dict, alias: str, raw: dict) -> dict:
    extraction = Extraction.model_validate_json(response_text(raw))
    valid_ids = {p["id"] for p in essay["paragraphs"]}
    dropped = []

    entities = []
    for ent in extraction.entities:
        item = ent.model_dump()
        if ent.type not in ENTITY_TYPES:
            dropped.append({"item": item, "reason": "bad_type"})
            continue
        good = [pid for pid in ent.paragraphs if pid in valid_ids]
        for pid in ent.paragraphs:
            if pid not in valid_ids:
                dropped.append({"item": {"entity": ent.name, "paragraph": pid}, "reason": "bad_paragraph"})
        if not good:
            continue
        entities.append({**item, "paragraphs": good})

    known = {e["name"] for e in entities} | {AUTHOR}
    relations = []
    for rel in extraction.relations:
        item = rel.model_dump()
        if rel.kind not in RELATION_KINDS:
            reason = "bad_kind"
        elif rel.source not in known or rel.target not in known:
            reason = "unknown_entity"
        else:
            reason = check_quote(essay, rel.paragraph, rel.quote)
        if reason:
            dropped.append({"item": item, "reason": reason})
        else:
            relations.append(item)

    eid = essay["id"]
    meta = essay["meta"]
    usage = {k: raw["usage"][k] for k in ("input_tokens", "output_tokens")}
    return {
        "essay": {
            "id": eid,
            "number": meta["number"],
            "slug": meta["slug"],
            "title": meta["title"],
            "source": meta["source"],
        },
        "author": {"name": AUTHOR},
        "model": raw["model"],
        "alias": alias,
        "paragraphs": [{"id": p["id"], "global_id": f"{eid}#{p['id']}", "text": p["text"]} for p in essay["paragraphs"]],
        "entities": entities,
        "relations": relations,
        "mentioned_in": [
            {"entity": e["name"], "essay": eid, "paragraphs": [f"{eid}#{pid}" for pid in e["paragraphs"]]}
            for e in entities
        ],
        "dropped": dropped,
        "usage": usage,
        "cost_usd": cost_usd(raw["model"], usage),
    }


# --- rendering ---


def _quote_block(text: str) -> str:
    return "\n".join(f"> {line}" for line in text.splitlines() or [""])


def render_review(result: dict) -> str:
    e = result["essay"]
    out = [
        f"# {e['id']}: {e['title']}",
        "",
        f"model: {result['model']} · source: {e['source']}",
        f"entities: {len(result['entities'])} · relations: {len(result['relations'])} · "
        f"dropped: {len(result['dropped'])} · tokens: {result['usage']['input_tokens']} in / "
        f"{result['usage']['output_tokens']} out · ${result['cost_usd']:.4f}",
        "",
    ]
    for etype in ENTITY_TYPES:
        group = [x for x in result["entities"] if x["type"] == etype]
        if not group:
            continue
        out += [f"## {etype}", ""]
        for ent in group:
            aliases = f" (also: {', '.join(ent['aliases'])})" if ent["aliases"] else ""
            out.append(f"- **{ent['name']}**{aliases}: {ent['description']} [{', '.join(ent['paragraphs'])}]")
        out.append("")

    out += ["## relations", ""]
    for rel in result["relations"]:
        out += [
            f"- {rel['source']} —{rel['kind']} ({rel['label']})→ {rel['target']} [{rel['paragraph']}]",
            "",
            _quote_block(rel["quote"]),
            "",
        ]

    out += ["## dropped", ""]
    if not result["dropped"]:
        out.append("none")
    for d in result["dropped"]:
        out.append(f"- `{d['reason']}`: {json.dumps(d['item'], ensure_ascii=False)}")
    return "\n".join(out).rstrip() + "\n"


def _counts(counter: Counter, order: list[str] | None = None) -> str:
    keys = order or sorted(counter)
    parts = [f"{k} {counter[k]}" for k in keys if counter[k]]
    return ", ".join(parts) or "–"


def render_compare(results: list[dict]) -> str:
    out = [
        "# extraction pilot: essay × model",
        "",
        "| essay | model | entities by type | relations by kind | dropped by reason | tokens in / out | cost |",
        "|---|---|---|---|---|---|---|",
    ]
    total = 0.0
    for r in sorted(results, key=lambda r: (r["essay"]["id"], r["alias"])):
        ents = Counter(e["type"] for e in r["entities"])
        rels = Counter(x["kind"] for x in r["relations"])
        drops = Counter(d["reason"] for d in r["dropped"])
        total += r["cost_usd"]
        out.append(
            f"| {r['essay']['id']} | {r['alias']} | {_counts(ents, ENTITY_TYPES)} ({sum(ents.values())}) "
            f"| {_counts(rels, RELATION_KINDS)} ({sum(rels.values())}) | {_counts(drops)} ({sum(drops.values())}) "
            f"| {r['usage']['input_tokens']} / {r['usage']['output_tokens']} | ${r['cost_usd']:.4f} |"
        )
    out += ["", f"total cost: ${total:.4f}"]
    return "\n".join(out) + "\n"


# --- running ---


def call_model(client, model_id: str, essay: dict) -> dict:
    response = client.messages.parse(
        model=model_id,
        max_tokens=MAX_TOKENS,
        system=SYSTEM,
        messages=[{"role": "user", "content": build_prompt(essay)}],
        output_config={"effort": EFFORT},
        output_format=Extraction,
    )
    return response.model_dump(mode="json")


def run_one(md_path: Path, alias: str, out_dir: Path, client, force: bool) -> dict:
    essay = parse_essay(md_path.read_text(encoding="utf-8"))
    raw_path = out_dir / "raw" / alias / f"{essay['id']}.json"

    if raw_path.exists() and not force:
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
    else:
        raw = call_model(client, MODELS[alias], essay)
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

    if raw.get("stop_reason") not in ("end_turn", None):
        raise RuntimeError(f"{essay['id']} on {alias}: stop_reason={raw.get('stop_reason')}")

    result = build_result(essay, alias, raw)
    model_dir = out_dir / alias
    model_dir.mkdir(parents=True, exist_ok=True)
    (model_dir / f"{essay['id']}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (model_dir / f"{essay['id']}.review.md").write_text(render_review(result), encoding="utf-8")
    return result


def run_all(paths: list[Path], aliases: list[str], out_dir: Path, client, force: bool) -> tuple[list[dict], int]:
    """Run every essay × model. Keeps going on per-call errors, stops at once on a bad key."""
    import anthropic

    results, failed = [], 0
    for path in paths:
        for alias in aliases:
            try:
                r = run_one(path, alias, out_dir, client, force)
            except anthropic.AuthenticationError as exc:
                # the message names the problem, never the key itself
                print(f"{path.stem} {alias}: ERROR authentication failed ({exc.message}); stopping", file=sys.stderr)
                raise SystemExit(1)
            except Exception as exc:
                failed += 1
                print(f"{path.stem} {alias}: ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
                continue
            results.append(r)
            print(f"{r['essay']['id']} {alias}: {len(r['entities'])} entities, "
                  f"{len(r['relations'])} relations, {len(r['dropped'])} dropped, ${r['cost_usd']:.4f}")
    return results, failed


def find_essays(data_dir: Path, numbers: list[int]) -> list[Path]:
    paths = []
    for n in numbers:
        found = sorted((data_dir / "essays_md").glob(f"{n:03d}_*.md"))
        if len(found) != 1:
            print(f"Error: expected one essays_md/{n:03d}_*.md, found {len(found)}", file=sys.stderr)
            raise SystemExit(1)
        paths.append(found[0])
    return paths


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extraction pilot on parallelmuhit essays")
    parser.add_argument("--essays", default=",".join(map(str, PILOT_ESSAYS)), help="comma-separated essay numbers")
    parser.add_argument("--model", choices=["haiku", "sonnet", "both"], default="both")
    parser.add_argument("--force", action="store_true", help="call the api even if a raw response is cached")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    return parser.parse_args(argv)


def main():
    args = parse_args()
    numbers = [int(x) for x in args.essays.split(",") if x.strip()]
    aliases = list(MODELS) if args.model == "both" else [args.model]
    paths = find_essays(args.data_dir, numbers)

    client = None

    def get_client():
        nonlocal client
        if client is None:
            import anthropic

            client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
        return client

    class LazyClient:
        @property
        def messages(self):
            return get_client().messages

    results, failed = run_all(paths, aliases, args.out_dir, LazyClient(), args.force)
    if results:
        (args.out_dir / "compare.md").write_text(render_compare(results), encoding="utf-8")
        print(f"\ncompare: {args.out_dir / 'compare.md'}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
