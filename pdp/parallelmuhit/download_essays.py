#!/usr/bin/env python3
"""
Download all parallelmuhit.uz essays as PDFs via the API.

Usage:
    TOKEN=<your_jwt> python3 download_essays.py            # all essays
    TOKEN=<your_jwt> python3 download_essays.py --number 5 # essay #5 only
    python3 download_essays.py --token <jwt> --number 42
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

import httpx
from playwright.async_api import async_playwright

API_BASE = "https://b.parallelmuhit.uz"
OUTPUT_DIR = Path("essays")

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: Georgia, "Times New Roman", serif;
    font-size: 16px;
    line-height: 1.85;
    color: #1a1a1a;
    max-width: 680px;
    margin: 0 auto;
    padding: 48px 24px;
  }}
  h1 {{
    font-size: 1.75em;
    line-height: 1.3;
    margin-bottom: 0.4em;
  }}
  .meta {{
    color: #888;
    font-size: 0.88em;
    font-style: italic;
    margin-bottom: 2.5em;
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 1em;
  }}
  .content p {{ margin-bottom: 1.15em; }}
  .content img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1.5em auto;
  }}
  .content a {{ color: #444; }}
  .content blockquote {{
    border-left: 3px solid #ccc;
    padding-left: 1em;
    margin: 1em 0;
    color: #555;
  }}
</style>
</head>
<body>
  <h1>{title}</h1>
  <p class="meta">{author} &nbsp;·&nbsp; #{number}</p>
  <div class="content">{content}</div>
</body>
</html>"""


def safe_filename(slug: str, index: int) -> str:
    return f"{index:03d}_{slug}.pdf"


async def download_essays(token: str, only: int | None = None, range_: tuple[int, int] | None = None):
    OUTPUT_DIR.mkdir(exist_ok=True)

    api_headers = {
        "Authorization": f"Bearer {token}",
        "token": token,
        "Origin": "https://parallelmuhit.uz",
        "Referer": "https://parallelmuhit.uz/",
    }

    print("Fetching essay list...")
    async with httpx.AsyncClient(headers=api_headers, timeout=30) as client:
        resp = await client.get(f"{API_BASE}/blog")
        resp.raise_for_status()
        raw = resp.json()

    # Sort oldest-first and assign site numbers (rank + 1 to match the site's
    # numbering, which counts one deleted/hidden essay not returned by the API)
    essays = [
        {**e, "site_number": i + 1}
        for i, e in enumerate(sorted(raw, key=lambda e: e["createdAt"]), start=1)
    ]

    print(f"Found {len(essays)} essays\n")

    total = len(essays)
    max_num = essays[-1]["site_number"]
    if only is not None:
        matched = [e for e in essays if e["site_number"] == only]
        if not matched:
            print(f"Error: no essay with site number {only} (valid range: 2–{max_num})", file=sys.stderr)
            sys.exit(1)
        essays = matched
    elif range_ is not None:
        start, end = range_
        essays = [e for e in essays if start <= e["site_number"] <= end]
        if not essays:
            print(f"Error: no essays in range {start}–{end}", file=sys.stderr)
            sys.exit(1)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        async with httpx.AsyncClient(headers=api_headers, timeout=30) as client:
            for essay in essays:
                i = essay["site_number"]
                slug = essay["slug"]
                title = essay.get("title", slug)
                author = essay.get("author", {}).get("name", "")
                filename = OUTPUT_DIR / safe_filename(slug, i)

                if filename.exists():
                    print(f"[{i:3d}/{total}] skip  {slug}")
                    continue

                print(f"[#{i:3d}/{total+1}] {title[:52]:<54} → {filename.name}")
                try:
                    r = await client.get(f"{API_BASE}/blog/slug/{slug}")
                    r.raise_for_status()
                    content = r.json().get("content", "")

                    html = HTML_TEMPLATE.format(
                        title=title,
                        author=author,
                        number=i,
                        content=content,
                    )
                    # networkidle waits for images (hosted on b.parallelmuhit.uz) to load
                    await page.set_content(html, wait_until="networkidle", timeout=30_000)
                    await page.pdf(
                        path=str(filename),
                        format="A4",
                        print_background=True,
                        margin={"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"},
                    )
                except Exception as exc:
                    print(f"          ERROR: {exc}")

        await browser.close()

    print(f"\nDone. PDFs saved to ./{OUTPUT_DIR}/")


def main():
    parser = argparse.ArgumentParser(description="Download parallelmuhit.uz essays as PDFs")
    parser.add_argument("--token", default=os.environ.get("TOKEN", ""), help="JWT auth token")
    parser.add_argument("--number", type=int, default=None, metavar="N", help="download only essay #N")
    parser.add_argument("--range", dest="range_", metavar="A-B", help="download essays #A through #B (e.g. 166-170)")
    args = parser.parse_args()

    if not args.token:
        print("Error: provide your JWT token via --token or TOKEN env var", file=sys.stderr)
        sys.exit(1)

    range_ = None
    if args.range_:
        try:
            a, b = args.range_.split("-")
            range_ = (int(a), int(b))
        except ValueError:
            print("Error: --range must be in the form A-B (e.g. 166-170)", file=sys.stderr)
            sys.exit(1)

    asyncio.run(download_essays(args.token, only=args.number, range_=range_))


if __name__ == "__main__":
    main()
