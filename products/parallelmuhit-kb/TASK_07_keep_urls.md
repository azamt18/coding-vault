# task 07: keep the urls the essays link to

written 2026-11-12 by the plan session. found by the user in the ui: "Shahboz Dolimov bilan suhbatga qarang." is `<a href=youtube…>qarang</a>` in the original, and the graph shows plain text.

## cause

`extract.py` `plain_text()` turns `[qarang](https://…)` into `qarang`. the markdown export (task 01) is fine: 2239 links in 182 of 188 essays are in `pdp/parallelmuhit/essays_md/`. only the extraction/graph layer drops them.

## goal

every url the author put in an essay is shown in the ui next to the quote it belongs to, and is available to the rag (task 08) for citations.

## rules (code only, no model calls, no re-extraction)

1. `parse_essay` also returns `links` per paragraph: `[{"text": anchor, "url": url}]`, read from the markdown before `plain_text` strips it. only `http(s)` urls. images are not links. paragraph ids and `text` stay byte-identical, so every existing quote still matches.
2. do not rerun `claude -p`. the existing `extract/sonnet/*.json` keep their entities and relations. a small offline step re-parses `essays_md/` and writes `links` into each paragraph of the extraction output, matched by `global_id`. fail loudly if a paragraph text no longer matches.
3. in `graph*.json`:
   - a relation link gets `urls` = the paragraph's links whose anchor text occurs inside its `quote`. (for p13 of 003_javoblar: Aziz Rahimov → Shahboz Dolimov gets the youtube url, anchor "qarang".)
   - a `mentioned_in` link gets all of its paragraph's urls.
   - a node gets `urls` when a link's anchor text equals its name, base_name or an alias (casefolded, apostrophe-normalised as in `merge_names.py`). typical: `[Atomic Habits](…)`. the anchor "qarang" matches no node, and that is fine.
   - dedupe by url. keep the order of appearance.
4. the graph schema change is additive: old keys unchanged, `urls` omitted when empty.

## ui

- in the node panel, a quote shows its urls as `↗ anchor` links (`target=_blank`, `rel="noopener noreferrer"`). a node with `urls` shows them under its description.
- no change to filters or layout.

## tests

- python: a markdown block with a link, an image, a mailto and two links with the same url → right `links`; paragraph text unchanged; the 003_javoblar p13 case end to end; rerun is byte-identical.
- npm: the panel renders `urls`, and renders nothing when absent.
- all existing tests still pass (114 python, 23 npm).

## acceptance (plan checks)

- p13 of 003_javoblar shows the youtube link in the ui.
- count: urls in `essays_md` (2239 occurrences) vs urls reaching the graph. report how many were attached and how many were left out (anchor not inside any quote and not a node name), so the user sees the loss. the number is reported, not forced to zero.
- `claude -p` was not called (usage unchanged).
