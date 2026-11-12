# parallelmuhit kb: status

updated 2026-11-12 by "Parallel muhit KB on RAG (plan)". this file is the plan session's memory. the details are in the TASK_*.md files.

## goal

a visual tool that shows how the people, works, ideas and organizations in Aziz Rahimov's 188 parallelmuhit.uz essays relate to each other, with every link backed by a quote. q&a over the graph (rag) comes later.

## setup

- sessions: "Parallel muhit KB on RAG (plan)" plans and verifies, "… (impl)" codes and commits. hand-offs are pointers to a TASK section.
- branch `feat/pm-kb` (started from feat/savolbor, so it needs a rebase onto main before any pr). a tts session also commits there (`products/parallelmuhit-tts`), so leave its files alone. no push/merge/pr without the user's ok.
- data: `pdp/parallelmuhit/` (essays pdf, `essays_md/`, `essays_raw/`, gitignored). code: `products/parallelmuhit-kb/`. extraction output: `products/parallelmuhit-kb/extract/` (gitignored).
- model calls: `claude -p` on the user's subscription (no anthropic api key, only openrouter). the subscription's 5-hour limit holds about 20 sonnet essays per window, and runs resume from the raw cache.

## decisions

- the author of all 188 is Aziz Rahimov. the api's author is `posted_by`.
- extraction: sonnet 5.5, one call per essay, numbered paragraphs. entities person/work/idea/organization with `name` (verbatim) + `base_name`. 7 link kinds (wrote, recommends, criticises, inspired_by, example_of, counterexample_of, associated_with, the last only as a last resort). the quote is 1–3 sentences, an exact substring. every person/work has ≥1 link.
- link endpoints match name/base_name case-insensitively.
- the essay, author and mentioned_in pieces are built by code.

## done

- task 01 markdown export: 188 essays.
- task 02 pilot (3 essays, 3 rounds).
- task 04 merge names: `f0ffbf0`. 1948 nodes (542 persons, 145 works, 73 orgs, 999 ideas), 119 blocks clustered by the model, 3 compound splits. relation links 2193 = 2190 + 3 − 0 self-loops, 0 dangling, 102 tests. checked by plan 2026-11-12: munger/taleb/buffet each one node (Ernst Buffet kept separate), 0 of 30 sampled merges wrong (seed 20261112), offline rerun byte-identical.
- task 03 full run: 2582 entities, 2190 links, drops 0.2%, associated_with 6.8%, 8 unlinked, 80 tests. last code `d331b93`, closed `84344e7`.

## known weaknesses

- about 10% of links are weak: the quote doesn't name the source, a forced kind, a heading as an entity.
- `inspired_by` runs in both directions (person draws on source, idea comes from person).

## decisions, task 04 (user: "yes" to all, 2026-11-12)

- merge only persons/works/orgs. ideas merge on an exact base_name only, and real grouping comes in task 05.
- code blocks candidates, then sonnet clusters each block via `claude -p`, keeping names apart when unsure.
- split compound names when every part is a known entity, copying the links to each part.
- the label is the spelling used in the most essays.
- `merge_overrides.json` (tracked, the user edits it) is applied on every run.
- the output is one `extract/graph.json`, with no sqlite.

## decisions, task 05 (user, 2026-11-12)

- scope: only ideas in 2+ essays (70 of 999). the other 929 stay as they are, no theme. known weakness: the graph's idea layer barely changes, and a 1-essay idea can't join a theme. revisit after seeing the result.
- shape: merge variants, then group the merged ideas under about 5–15 themes (theme nodes + `in_theme` links).
- method: sonnet via `claude -p`, same as task 04, no embeddings.

## done, task 05 group ideas: `df44bcd` (checked by plan 2026-11-12)

- 70 ideas in ≥2 essays → 69 (1 merge: SI → Sun'iy intellekt, correct). 14 themes, every idea has exactly 1 in_theme. `extract/graph_grouped.json`: 1961 nodes, 5035 links = 4966 − 0 − 0 folded + 69. 0 dangling, 114 tests, offline rerun byte-identical (`18df51b2ce8f`).
- the 20-merge sample can't be drawn (only 1 merge). the model is cautious by design ("when unsure keep apart").

## open for the user (not blocking)

- idea merges the model left apart, which could go into `idea_overrides.json`: hikmat + hikmat egasi, Mimesis + mimetik qaramlik, Status + Status o'yinlari, kutilma + Kichik kutuvlar. opposites stay apart (moliyaviy erkinlik / qaramlik).
- themes that look off: omad and Serendipity under "Ish samaradorligi", "Asperger sindromi" under "Mustaqil fikr", "umumiy kontekst" under "Foydalilik", "Tasavvur" under "Hikmat". "Hasad" ← Ijtimoiy tarmoqlar / Qarz to'foni fits if the essays tie them to comparison.
- name overrides from task 04: labels "Charli Manger", "Baffet", "Andryu Gryu", and the missed "Umar hazratlari" → Umar.

## decisions, task 06 (user, 2026-11-12)

- local only for now, publishing later (so: static site, one data-path constant).
- features, all four: node details with quotes, filters (type/kind/essay), search, neighbourhood focus.
- weak links shown as they are.
- stack: user delegated, so vite + ts + graphology + sigma, vanilla, in `ui/`.

## next: task 06 (written, `TASK_06_graph_ui.md`)

- hand-off to impl: "do TASK_06_graph_ui.md".
- this STATUS.md update is not committed. impl commits it with task 06.
- worktree: `/Users/azam_turgunboev/coding-vault-pmkb` (feat/pm-kb), not pushed. a rebase onto main is needed before any pr.
