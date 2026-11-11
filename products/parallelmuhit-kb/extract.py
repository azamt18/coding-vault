#!/usr/bin/env python3
"""
Extraction pilot: pull entities and quote-backed relations out of essays with Claude.

One call per essay per model. The model sees the title and numbered plain-text
paragraphs; each relation carries a quote of 1-3 consecutive sentences from one
paragraph. Code checks every relation against the essay and drops (never fixes)
what doesn't hold, and counts persons/works left without a relation (unlinked). Code also builds the essay node, the author node and the
mentioned_in edges.

Usage:
    python3 extract.py                                  # pilot essays 2,149,180 on sonnet
    python3 extract.py --essays 149 --model haiku
    python3 extract.py --force                          # ignore cached raw responses

Backends: `cli` (default) runs `claude -p` on the user's Claude Code subscription
in an isolated, empty temp dir with the ANTHROPIC_* overrides removed; `sdk` uses
the Anthropic SDK with ANTHROPIC_API_KEY. Outputs go to extract/ next to this
script (gitignored): raw/<model>/NNN_slug.json, <model>/NNN_slug.json,
<model>/NNN_slug.review.md and compare.md.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, ValidationError

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

# claude -p isolation: no tools, no MCP, no user/project settings (so no CLAUDE.md, hooks,
# plugins or the settings' own API key), no skills, no saved session. --bare can't be used:
# it turns off the OAuth login the subscription needs.
CLI_FLAGS = [
    "-p",
    "--output-format", "json",
    "--tools", "",
    "--strict-mcp-config",
    "--setting-sources", "",
    "--disable-slash-commands",
    "--no-session-persistence",
    "--effort", EFFORT,
]
# any of these makes claude code use an api key (here: openrouter) instead of the subscription
CLI_ENV_DROP = ["ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_BASE"]
CLI_TIMEOUT_S = 900


class BadJson(Exception):
    """The model's answer is not valid json for the Extraction schema."""


class CliError(Exception):
    """claude -p itself failed (auth, model, timeout, non-json output)."""

ENTITY_TYPES = ["person", "work", "idea", "organization"]
RELATION_KINDS = [
    "wrote", "recommends", "criticises", "inspired_by", "example_of", "counterexample_of", "associated_with",
]


# --- response schema (type/kind stay plain strings so code, not the decoder, enforces the lists) ---


class Entity(BaseModel):
    name: str = Field(description="exactly as written in the essay")
    base_name: str = Field(description="basic form with normal capitals, the essay's spelling, not translated")
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
    emphasis, and turns non-breaking spaces into normal ones. Apostrophes and
    Uzbek letters are left byte for byte.
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
    # U+00A0 (from &nbsp;) reads as a normal space: models copy it back as one
    return re.sub(r"[ \t\u00a0]+", " ", text).strip()


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
- name: exactly as written in the essay, including its apostrophes, letters and lowercase.
  Do not capitalise or otherwise change it ("kibr" stays "kibr"); only base_name changes form.
- base_name: the same name in its basic form with normal capitals: no case or possessive
  endings, no titles like "janob" ("janob Talebda" -> "Taleb", "Teylor svift" -> "Teylor Svift",
  "prison break" -> "Prison Break"). Keep the essay's spelling and transliteration; do not
  translate it or switch to an English spelling. If the name is already basic, repeat it.
- type: one of {", ".join(ENTITY_TYPES)}.
  work = book, article, film, podcast or talk. Do not extract places or events.
- description: one sentence in Uzbek, based only on what the essay says.
- aliases: other spellings of the same entity in this essay (may be empty).
- paragraphs: ids of the paragraphs where it appears.
Do not list {AUTHOR} as an entity; refer to him by that name in relations.
Every person and every work must have at least one relation, to an idea, a person, a work or
{AUTHOR}. If the essay mentions someone to make a point, extract that point as an idea and
link them to it.

Relations: source --kind--> target, for example person wrote work, idea example_of idea.
Use counterexample_of when the essay holds someone or something up as the opposite of an
idea (a warning, what not to do), and example_of only when it is shown as a case of the idea.
Use associated_with only when none of the other 6 kinds fits. Usually another kind is meant:
the source of an idea or a thought (where it comes from, who taught it) -> inspired_by; advice
to do or read something -> recommends; a case of an idea -> example_of; the opposite of an
idea -> counterexample_of; disapproval -> criticises; authorship -> wrote.
- source and target: entity names from your list, or "{AUTHOR}".
- kind: one of {", ".join(RELATION_KINDS)}.
- label: a short phrase in Uzbek, using the essay's own wording.
- paragraph: the id of the paragraph that supports it.
- quote: 1-3 consecutive sentences from that paragraph that state the link, so that the quote
  alone makes the link clear: include the sentence that names the source or target when the
  link itself is stated in the next one. Copy it exactly, character for character, as one
  continuous piece of that paragraph. Do not change apostrophes (ʻ ‘ ’ ') or letters, and do
  not join text from different paragraphs.
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


LINKED_TYPES = ("person", "work")


def find_unlinked(entities: list[dict], relations: list[dict]) -> list[str]:
    """Persons and works that are neither source nor target of any kept relation."""
    ends = {r["source"] for r in relations} | {r["target"] for r in relations}
    return [e["name"] for e in entities if e["type"] in LINKED_TYPES and e["name"] not in ends]


def build_result(essay: dict, alias: str, raw: dict) -> dict:
    try:
        extraction = Extraction.model_validate_json(response_text(raw))
    except ValidationError as exc:
        raise BadJson(str(exc).splitlines()[0]) from exc
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
    backend = raw.get("backend", "sdk")
    if backend == "cli":
        cost, billed = raw.get("total_cost_usd"), False  # what claude code reports; the subscription pays
    else:
        cost, billed = cost_usd(raw["model"], usage), True
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
        "unlinked": find_unlinked(entities, relations),
        "usage": usage,
        "backend": backend,
        "billed": billed,
        "cost_usd": cost,
        "duration_ms": raw.get("duration_ms"),
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
        f"{result['usage']['output_tokens']} out · {_cost_label(result)}",
        "",
    ]
    for etype in ENTITY_TYPES:
        group = [x for x in result["entities"] if x["type"] == etype]
        if not group:
            continue
        out += [f"## {etype}", ""]
        for ent in group:
            aliases = f" (also: {', '.join(ent['aliases'])})" if ent["aliases"] else ""
            base = f" → {ent['base_name']}" if ent.get("base_name") and ent["base_name"] != ent["name"] else ""
            out.append(f"- **{ent['name']}**{base}{aliases}: {ent['description']} [{', '.join(ent['paragraphs'])}]")
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

    out += ["", "## unlinked", "", "persons and works with no relation (counted, not dropped):", ""]
    unlinked = result.get("unlinked", [])
    out += [f"- {name}" for name in unlinked] or ["none"]
    return "\n".join(out).rstrip() + "\n"


def _counts(counter: Counter, order: list[str] | None = None) -> str:
    keys = order or sorted(counter)
    parts = [f"{k} {counter[k]}" for k in keys if counter[k]]
    return ", ".join(parts) or "–"


def _cost_label(r: dict) -> str:
    if r["cost_usd"] is None:
        return "–"
    label = f"${r['cost_usd']:.4f}"
    return label if r.get("billed", True) else f"{label} (subscription, not billed)"


def _seconds(r: dict) -> str:
    return f"{r['duration_ms'] / 1000:.1f} s" if r.get("duration_ms") is not None else "–"


def _unlinked_cell(r: dict) -> str:
    names = r.get("unlinked", [])
    return f"{len(names)} ({', '.join(names)})" if names else "0"


def render_compare(results: list[dict]) -> str:
    out = [
        "# extraction pilot: essay × model",
        "",
        "| essay | model | entities by type | relations by kind | dropped by reason | unlinked | tokens in / out | run time | cost |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    total = 0.0
    for r in sorted(results, key=lambda r: (r["essay"]["id"], r["alias"])):
        ents = Counter(e["type"] for e in r["entities"])
        rels = Counter(x["kind"] for x in r["relations"])
        drops = Counter(d["reason"] for d in r["dropped"])
        total += r["cost_usd"] or 0.0
        out.append(
            f"| {r['essay']['id']} | {r['alias']} | {_counts(ents, ENTITY_TYPES)} ({sum(ents.values())}) "
            f"| {_counts(rels, RELATION_KINDS)} ({sum(rels.values())}) | {_counts(drops)} ({sum(drops.values())}) "
            f"| {_unlinked_cell(r)} "
            f"| {r['usage']['input_tokens']} / {r['usage']['output_tokens']} | {_seconds(r)} | {_cost_label(r)} |"
        )
    billed = all(r.get("billed", True) for r in results)
    out += ["", f"total cost: ${total:.4f}" + ("" if billed else " (subscription, not billed)")]
    return "\n".join(out) + "\n"


# --- running ---


def call_model_sdk(client, model_id: str, essay: dict) -> dict:
    response = client.messages.parse(
        model=model_id,
        max_tokens=MAX_TOKENS,
        system=SYSTEM,
        messages=[{"role": "user", "content": build_prompt(essay)}],
        output_config={"effort": EFFORT},
        output_format=Extraction,
    )
    return response.model_dump(mode="json")


def cli_prompt(essay: dict) -> str:
    schema = json.dumps(Extraction.model_json_schema(), ensure_ascii=False)
    return (
        build_prompt(essay)
        + "\n\nReply with only one JSON object that matches this JSON Schema."
        + " No prose before or after it, no code fences.\n"
        + schema
    )


def call_model_cli(model_id: str, essay: dict) -> dict:
    """Run claude -p on the subscription and return the answer in the sdk's raw shape."""
    env = {k: v for k, v in os.environ.items() if k not in CLI_ENV_DROP}
    args = ["claude", *CLI_FLAGS, "--model", model_id, "--system-prompt", SYSTEM]
    with tempfile.TemporaryDirectory(prefix="pm-extract-") as cwd:
        try:
            proc = subprocess.run(args, input=cli_prompt(essay), capture_output=True, text=True,
                                  env=env, cwd=cwd, timeout=CLI_TIMEOUT_S)
        except subprocess.TimeoutExpired as exc:
            raise CliError(f"timeout after {CLI_TIMEOUT_S} s") from exc
    try:
        out = json.loads(proc.stdout)
    except (json.JSONDecodeError, TypeError) as exc:
        raise CliError(f"exit {proc.returncode}, non-json output: {(proc.stdout or proc.stderr or '')[:200]}") from exc
    if out.get("is_error") or proc.returncode != 0:
        raise CliError(f"exit {proc.returncode}: {str(out.get('result'))[:200]}")

    u = out.get("usage") or {}
    return {
        "backend": "cli",
        "model": model_id,
        "models_used": sorted(out.get("modelUsage") or {}),
        "content": [{"type": "text", "text": out.get("result") or ""}],
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
            + u.get("cache_read_input_tokens", 0),
            "output_tokens": u.get("output_tokens", 0),
        },
        "duration_ms": out.get("duration_ms"),
        "total_cost_usd": out.get("total_cost_usd"),
        "cli_output": out,
    }


def run_one(md_path: Path, alias: str, out_dir: Path, client, force: bool, backend: str = "sdk") -> dict:
    essay = parse_essay(md_path.read_text(encoding="utf-8"))
    raw_path = out_dir / "raw" / alias / f"{essay['id']}.json"

    if raw_path.exists() and not force:
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
    else:
        if backend == "cli":
            raw = call_model_cli(MODELS[alias], essay)
        else:
            raw = call_model_sdk(client, MODELS[alias], essay)
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


def run_all(paths: list[Path], aliases: list[str], out_dir: Path, client, force: bool,
            backend: str = "sdk") -> tuple[list[dict], list[tuple[str, str, str]]]:
    """Run every essay × model. Keeps going on per-call errors (no retries), stops at once on a bad key."""
    import anthropic

    results, failures = [], []
    for path in paths:
        for alias in aliases:
            try:
                r = run_one(path, alias, out_dir, client, force, backend)
            except BadJson as exc:
                failures.append((path.stem, alias, "bad_json"))
                print(f"{path.stem} {alias}: ERROR bad_json: {exc}", file=sys.stderr)
                continue
            except CliError as exc:
                failures.append((path.stem, alias, "cli_error"))
                print(f"{path.stem} {alias}: ERROR cli_error: {exc}", file=sys.stderr)
                continue
            except anthropic.AuthenticationError as exc:
                # the message names the problem, never the key itself
                print(f"{path.stem} {alias}: ERROR authentication failed ({exc.message}); stopping", file=sys.stderr)
                raise SystemExit(1)
            except Exception as exc:
                failures.append((path.stem, alias, type(exc).__name__))
                print(f"{path.stem} {alias}: ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
                continue
            results.append(r)
            print(f"{r['essay']['id']} {alias}: {len(r['entities'])} entities, "
                  f"{len(r['relations'])} relations, {len(r['dropped'])} dropped, {_seconds(r)}, {_cost_label(r)}")
    return results, failures


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
    parser.add_argument("--model", choices=["haiku", "sonnet", "both"], default="sonnet")
    parser.add_argument("--backend", choices=["cli", "sdk"], default="cli",
                        help="cli: claude -p on the subscription (default); sdk: anthropic sdk + ANTHROPIC_API_KEY")
    parser.add_argument("--force", action="store_true", help="call the model even if a raw response is cached")
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

    results, failures = run_all(paths, aliases, args.out_dir, LazyClient(), args.force, args.backend)
    if results:
        (args.out_dir / "compare.md").write_text(render_compare(results), encoding="utf-8")
        print(f"\ncompare: {args.out_dir / 'compare.md'}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
