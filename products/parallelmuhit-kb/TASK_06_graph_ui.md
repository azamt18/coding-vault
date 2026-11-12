# task 06: local graph explorer (ui)

written 2026-11-12 by the plan session. decisions settled with the user, see STATUS.md "decisions, task 06".

## goal

a local web page that shows `extract/graph_grouped.json` as an interactive graph, so the user can see how people, works, ideas and organizations in the essays relate, and read the quote behind every link. local only for now; publishing comes later, so keep it a static site with no server code.

## stack (best-practice defaults, user delegated)

- vite + typescript, vanilla (no react), under `products/parallelmuhit-kb/ui/`.
- graphology (data model) + sigma.js (webgl rendering) + graphology-layout-forceatlas2 (layout, run in a worker). about 2000 nodes and 5000 links is too many for svg or canvas.
- the page loads one json file with `fetch`. the path is a single constant, default `/graph_grouped.json`, so publishing later only changes that.
- a script `ui/sync_data.sh` copies `../extract/graph_grouped.json` to `ui/public/` (gitignored). `npm run dev` serves it. no backend.

## features (all required)

1. **graph view.** node colour by type (person, work, idea, organization, essay, theme, author), node size by `mention_count` (essays by degree). edge colour by `kind`. every link is shown as it is, weak ones included, no hiding or dimming.
2. **node details.** click a node: a side panel with label, type, aliases, theme (for ideas), per-essay descriptions, and a list of its links grouped by kind. each link shows the other end, the essay id, the paragraph and the full quote. click an other end to jump to it.
3. **filters.** checkboxes per node type and per link kind; an essay dropdown that keeps only links from that essay (and the nodes they touch). filters combine.
4. **search.** a text box matching label and aliases, casefolded and ignoring apostrophe forms (reuse the normalization idea from `merge_names.py`: ‘ ʻ ' ’ `). picking a result centres and selects the node.
5. **neighbourhood focus.** selecting a node dims everything except it and its direct neighbours; a button clears it.

## layout notes

- 188 essay nodes and 5000 links will be a hairball: start with essay nodes hidden and `mentioned_in`/`wrote` links hidden by default (they are filters the user can switch on, not removed).
- keep the ui in lowercase uzbek-neutral english labels; quotes stay as written.

## tests

- pure functions in `ui/src/` (search normalization, filter logic, neighbourhood computation) get unit tests with vitest, no browser.
- one smoke test: the page's data loader parses `graph_grouped.json` and every link endpoint is a node id.
- manual check list in `ui/README.md` (see acceptance).

## acceptance (the plan session checks)

- `npm test` passes; python tests still pass (114).
- `npm run build` succeeds; `npm run dev` shows the graph with the default filters.
- search "munger" finds one person node; selecting it shows its links with quotes.
- an essay filter, a type filter and a kind filter each change the visible graph, and combined filters give the intersection.
- the weak-link rule holds: no link is hidden unless a filter excludes its kind or type.
- no console errors on load.

## don't

- don't touch python code, `extract/` or the graph schema. if the ui needs a schema change, stop and write it in STATUS.md.
- no backend, no sqlite, no rag, no auth, no deploy config.
- don't commit `node_modules/`, `dist/` or `ui/public/graph_grouped.json`.
- commit only `products/parallelmuhit-kb/` paths, on `feat/pm-kb`. no push.
