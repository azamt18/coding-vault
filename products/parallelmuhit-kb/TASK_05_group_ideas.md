# task 05: group ideas (merge + themes)

written 2026-11-12 by the plan session. decisions settled with the user, see STATUS.md "decisions, task 05".

## goal

take the idea nodes in `extract/graph.json` that appear in 2 or more essays (70 of 999) and (a) merge variants of the same idea into one node, (b) put the merged ideas under about 5–15 broader themes. the visual tool can then show either level.

## inputs and outputs

- in: `extract/graph.json` (task 04 output, read only).
- new code: `group_ideas.py` + `test_group_ideas.py` in `products/parallelmuhit-kb/`.
- out (gitignored, under `extract/ideas/`): `candidates.json`, `raw/` (cached cli responses), `clusters.json`, `themes.json`, `ideas_summary.md`, and `extract/graph_grouped.json` (task 04's `graph.json` stays untouched).
- tracked: `idea_overrides.json` (the user edits it, it starts empty).

## steps

1. **select.** idea nodes with `len(essays) >= 2`. all other ideas pass through unchanged, with no theme. count both groups.
2. **merge (sonnet via `claude -p`).** one call for all selected ideas if they fit, otherwise blocks of at most 40 by first letter. same cli flags, env scrubbing, temp cwd and cache/resume behaviour as `merge_names.py` (reuse, don't copy). the prompt gives each idea with its label, aliases, one description per essay and the essay count. the model returns clusters of the given labels, json only. rules: merge only when it is the same idea; when unsure keep apart; reject any cluster that names a label not in the input (count it).
3. **themes (sonnet, one call).** input: the merged ideas (label + one description). output: 5–15 themes, each with a short uzbek name and the list of idea labels; every idea in exactly one theme. an idea that fits nothing goes to a theme named "boshqa". reject unknown labels, duplicates and missing ideas (count each).
4. **canonical label.** same rule as task 04: the spelling used in the most essays, tie goes to the longer form.
5. **overrides.** `idea_overrides.json` has `merge`, `keep_apart`, `label` (as in task 04) and `theme` (idea label → theme name). unknown names are a warning, not a crash.
6. **build `graph_grouped.json`.** merged idea nodes keep `aliases`, `descriptions`, `essays`, `mention_count` (union/sum), and get a `theme` field. links that pointed at a merged idea are repointed; a link whose ends become the same node is dropped and counted. add theme nodes (`type: theme`) and `in_theme` links from each idea. `--offline` rebuilds from the cache.
7. **`ideas_summary.md`.** counts before/after, rejected counts, every merge on one line, every theme with its ideas, so the user can skim and write overrides.

## tests (no model calls)

- selection: only ideas in 2+ essays are selected, the others pass through unchanged.
- cluster parsing: valid, unknown label, bad json. theme parsing: valid, duplicate, missing idea, unknown label.
- label choice and tie-break.
- overrides: merge, keep_apart, label, theme, unknown name.
- graph build: link count = input links − self-loops − folded mentioned_in + in_theme (decided 2026-11-12: two mentioned_in links between the same idea and essay are folded into one, with paragraphs unioned), no dangling endpoints, every merged idea has exactly one `in_theme` link.
- a fake cli response fixture.

## acceptance (the plan session checks)

- all tests pass, and the old 102 still pass.
- every selected idea has a theme; the sample of 20 merges (seed 20261112) has at most 1 wrong.
- link totals balance, 0 dangling.
- `--offline` rerun is byte-identical.

## don't

- don't touch `extract/sonnet/`, `graph.json` or the name merging.
- no embeddings, no new dependency, no sqlite, no ui.
- commit only `products/parallelmuhit-kb/` paths, on `feat/pm-kb`. no push.
