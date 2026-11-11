#!/usr/bin/env python3
"""
Export parallelmuhit.uz essays from the API to Markdown.

Raw API responses go to essays_raw/ (the list as _list.json, each essay as
NNN_slug.json), Markdown with YAML frontmatter goes to essays_md/NNN_slug.md.

Usage:
    TOKEN=<your_jwt> python3 export_markdown.py              # all essays
    TOKEN=<your_jwt> python3 export_markdown.py --number 5   # essay #5 only
    python3 export_markdown.py --token <jwt> --range 166-170
    python3 export_markdown.py --offline --force             # rebuild from essays_raw/, no token
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify

API_BASE = "https://b.parallelmuhit.uz"
SITE_BASE = "https://parallelmuhit.uz"
RAW_DIR = Path("essays_raw")
MD_DIR = Path("essays_md")
LIST_FILE = RAW_DIR / "_list.json"


def number_essays(raw: list[dict]) -> list[dict]:
    """Same numbering as download_essays.py: oldest first, rank + 1."""
    return [
        {**e, "site_number": i + 1}
        for i, e in enumerate(sorted(raw, key=lambda e: e["createdAt"]), start=1)
    ]


def select_essays(essays: list[dict], only: int | None = None, range_: tuple[int, int] | None = None) -> list[dict]:
    if only is not None:
        return [e for e in essays if e["site_number"] == only]
    if range_ is not None:
        start, end = range_
        return [e for e in essays if start <= e["site_number"] <= end]
    return essays


def filename_for(essay: dict, ext: str) -> str:
    return f"{essay['site_number']:03d}_{essay['slug']}{ext}"


def _prepare(html: str) -> str:
    """Join source line breaks inside text and make site-relative src/href absolute."""
    soup = BeautifulSoup(html, "html.parser")
    for text in soup.find_all(string=True):
        if text.find_parent(["pre", "code"]) is None and "\n" in text:
            text.replace_with(re.sub(r"\s*\n\s*", " ", text))
    for tag, attr, base in (("img", "src", API_BASE), ("a", "href", SITE_BASE)):
        for el in soup.find_all(tag):
            value = el.get(attr)
            if value and value.startswith("/") and not value.startswith("//"):
                el[attr] = base + value
    return str(soup)


def html_to_markdown(html: str) -> str:
    md = markdownify(
        _prepare(html),
        heading_style="ATX",
        bullets="-",
        escape_misc=False,
        escape_asterisks=False,
        escape_underscores=False,
    )
    lines = [line.rstrip() for line in md.splitlines()]
    md = "\n".join(lines)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def frontmatter(meta: dict) -> str:
    dumped = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=10_000)
    return f"---\n{dumped}---\n"


def render_essay(essay: dict, detail: dict) -> str:
    title = essay.get("title") or essay["slug"]
    meta = {
        "number": essay["site_number"],
        "slug": essay["slug"],
        "title": title,
        "author": (essay.get("author") or {}).get("name", ""),
        "created_at": essay["createdAt"],
        "source": f"{SITE_BASE}/{essay['slug']}",
    }
    body = html_to_markdown(detail.get("content") or "")
    return f"{frontmatter(meta)}\n# {title}\n\n{body}\n"


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "token": token,
        "Origin": SITE_BASE,
        "Referer": f"{SITE_BASE}/",
    }


def _write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def export(token: str, only: int | None, range_: tuple[int, int] | None, force: bool, offline: bool) -> int:
    RAW_DIR.mkdir(exist_ok=True)
    MD_DIR.mkdir(exist_ok=True)
    client = None

    if offline:
        if not LIST_FILE.exists():
            print(f"Error: --offline needs {LIST_FILE}; run once with a token first", file=sys.stderr)
            return 1
        raw = json.loads(LIST_FILE.read_text(encoding="utf-8"))
    else:
        import httpx

        client = httpx.Client(headers=_headers(token), timeout=30)
        print("Fetching essay list...")
        resp = client.get(f"{API_BASE}/blog")
        resp.raise_for_status()
        raw = resp.json()
        _write_json(LIST_FILE, raw)

    essays = number_essays(raw)
    print(f"Found {len(essays)} essays\n")
    selected = select_essays(essays, only, range_)
    if not selected:
        print("Error: no essays match --number/--range", file=sys.stderr)
        return 1

    errors = 0
    try:
        for essay in selected:
            n = essay["site_number"]
            md_path = MD_DIR / filename_for(essay, ".md")
            raw_path = RAW_DIR / filename_for(essay, ".json")

            if md_path.exists() and not force:
                print(f"[#{n:3d}] skip  {md_path.name}")
                continue

            try:
                if raw_path.exists():
                    detail = json.loads(raw_path.read_text(encoding="utf-8"))
                elif offline:
                    print(f"[#{n:3d}] ERROR: no {raw_path} for offline mode")
                    errors += 1
                    continue
                else:
                    r = client.get(f"{API_BASE}/blog/slug/{essay['slug']}")
                    r.raise_for_status()
                    detail = r.json()
                    _write_json(raw_path, detail)

                md_path.write_text(render_essay(essay, detail), encoding="utf-8")
                print(f"[#{n:3d}] {md_path.name}")
            except Exception as exc:  # keep going, report at the end
                # the exception text can hold the request, but never the token header
                print(f"[#{n:3d}] ERROR: {type(exc).__name__}: {exc}")
                errors += 1
    finally:
        if client is not None:
            client.close()

    print(f"\nDone. Markdown in ./{MD_DIR}/, raw JSON in ./{RAW_DIR}/" + (f" ({errors} errors)" if errors else ""))
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description="Export parallelmuhit.uz essays to Markdown")
    parser.add_argument("--token", default=os.environ.get("TOKEN", ""), help="JWT auth token (or TOKEN env var)")
    parser.add_argument("--number", type=int, default=None, metavar="N", help="export only essay #N")
    parser.add_argument("--range", dest="range_", metavar="A-B", help="export essays #A through #B (e.g. 166-170)")
    parser.add_argument("--force", action="store_true", help="overwrite existing .md files")
    parser.add_argument("--offline", action="store_true", help="convert from essays_raw/ without calling the API")
    args = parser.parse_args()

    if not args.offline and not args.token:
        print("Error: provide your JWT token via --token or TOKEN env var (or use --offline)", file=sys.stderr)
        sys.exit(1)

    range_ = None
    if args.range_:
        try:
            a, b = args.range_.split("-")
            range_ = (int(a), int(b))
        except ValueError:
            print("Error: --range must be in the form A-B (e.g. 166-170)", file=sys.stderr)
            sys.exit(1)

    sys.exit(export(args.token, args.number, range_, args.force, args.offline))


if __name__ == "__main__":
    main()
