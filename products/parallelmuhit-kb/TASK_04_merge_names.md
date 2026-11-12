# task 04: merge names into one graph

written 2026-11-12 by the plan session. decisions settled with the user (Q1–Q6, all "yes"), see STATUS.md.

## goal

turn the 188 per-essay extraction files (`extract/sonnet/*.json`) into one `extract/graph.json`, where each real person, work and organization is a single node, no matter how the essays spell it (charli munger / charlie munger / manger → one node). every link keeps its quote, paragraph and essay.

## inputs and outputs

- in: `extract/sonnet/*.json` (read only, never rewritten).
- new code: `merge_names.py` + `test_merge_names.py` in `products/parallelmuhit-kb/`.
- out (gitignored, under `extract/merge/`): `blocks.json`, `raw/` (cached cli responses), `clusters.json`, `merge_summary.md`, and `extract/graph.json`.
- tracked: `merge_overrides.json` in `products/parallelmuhit-kb/` (the user edits it, it starts empty).

## steps

1. **split compound names.** an entity whose base_name joins names with " va ", " & ", " hamda " or "," (for example "buffet va manger") is split only when every part already exists as an entity of the same type somewhere in the corpus. each link on the compound is copied to every part. the compound is left alone when any part is unknown. count splits and copied links.
2. **blocking (code, no model).** for person, work and organization separately, normalize base_name: casefold; drop the apostrophe forms ‘ ʻ ' ’ `; collapse double letters; fold common latin-uzbek spellings (ch/sh kept, "ye"→"e", "oo"/"u", "i"/"y", "ks"/"x", final "e" dropped). two names go in one block when their normalized last tokens match, or difflib ratio ≥ 0.8 on the normalized full forms (use union-find). singletons skip step 3. blocks over 40 names are split by first letter of the last token.
3. **cluster (sonnet via `claude -p`).** one call per block, with the same cli flags, env scrubbing and temp cwd as `extract.py` (reuse the code, don't copy it). the prompt gives each name with its type, one description, the essay count and one sample quote. the model returns clusters as lists of the given names, json only. rules in the system prompt: merge only when it is clearly the same real-world thing; when unsure keep them apart (over-merging is worse than a duplicate); a surname alone merges with a full name only if the descriptions agree. cache raw responses in `extract/merge/raw/<block>.json`; `--offline` rebuilds from the cache; `--jobs N`; stop cleanly on cli_error or a subscription limit, like `extract.py`. reject any cluster that names something not in the block (count it).
4. **canonical label.** the label is the spelling used in the most essays; on a tie, the longer form. all other spellings go to `aliases`.
5. **overrides.** `merge_overrides.json` has `merge` (lists of names to force into one node), `keep_apart` (lists that must not be merged) and `label` (node name → label). they apply after step 4 on every run, and an override naming an unknown entity is a warning, not a crash.
6. **ideas.** not clustered here (that is task 05). ideas merge only on an exact casefolded base_name.
7. **build `graph.json`.** `nodes`: `id` (stable slug of type + label), `label`, `type`, `aliases`, `descriptions` (one per essay, keyed by essay id), `essays`, `mention_count`. essay nodes and the author node as in the per-essay files. `links`: `source`, `target`, `kind`, `label`, `essay`, `paragraph`, `quote`, plus `wrote` and `mentioned_in` built by code. a link whose ends merge into the same node is dropped and counted (self-loop). same kind + same ends from different essays stay separate links (each has its own quote).
8. **`merge_summary.md`.** counts before/after per type; the counts of splits, self-loops and rejected clusters; the 20 largest clusters with all their spellings; the full list of merges (one line each), so the user can skim it and write overrides.

## tests (no model calls)

- normalization and blocking: munger variants share a block, unrelated names don't.
- compound split, both cases (all parts known / one part unknown).
- cluster parsing: valid response, a name outside the block, bad json.
- label choice and tie-break.
- overrides: merge, keep_apart, label, unknown name.
- graph build: link count = input links + copied links − self-loops; every link endpoint is a node id.
- a fixture with a fake cli response, like `fixtures/fake_extraction_response.json`.

## acceptance (the plan session checks)

- all tests pass, and the old 80 still pass.
- the known variants each become one node: munger, taleb, buffet.
- link totals balance (the step 7 formula), with 0 dangling endpoints.
- in a random sample of 30 merges (seed 20261112), at most 1 wrong merge.
- the rerun with `--offline` gives a byte-identical `graph.json`.

## don't

- don't touch `extract/sonnet/` or rerun extraction.
- don't cluster ideas.
- don't add sqlite or a ui.
- commit only `products/parallelmuhit-kb/` paths, and only on `feat/pm-kb`. no push.
