# task 03: extraction on all 188 essays

goal: a complete, checked set of extraction json files for all 188 essays, so task 04 (merging names across essays) can start. extraction stays as settled in task 02 (round 3). one prompt line changes.

decided with the user on 2026-11-11 (plan session).

## step 1: `associated_with` only as a last resort

- prompt: `associated_with` only when none of the other 6 kinds fits. say which kinds are usually meant instead (a source of an idea → `inspired_by`, advice → `recommends`).
- test first (the prompt contains the rule).
- back up the round 3 sonnet outputs to `extract/_prev_sonnet_r3/`. rerun `--essays 2,149,180 --model sonnet --force`.
- go/no-go for step 2: `associated_with` share of all links in the 3 essays clearly below round 3 (r3: 18 of 30 = 60%). 0 drops, 0 unlinked and 0 bad_json still hold. report to plan and **wait for plan's go**, then start step 2.

## step 2: full run

- `--essays all` (or a range). `--model sonnet`, `--backend cli`. the saved raw answers make it resumable: a rerun without `--force` only calls essays with no raw answer.
- **3 essays at a time** (`--jobs 3`, default 1). the output order and files are the same as a sequential run.
- **limits:** if a call fails because the subscription limit is hit (or any `cli_error`), stop starting new calls, let running ones finish, exit with a clear message. no waiting loops. the user reruns later.
- **broken answers:** after the run, retry each `bad_json` essay once with `--force` for that essay only. if it fails again, it stays `bad_json` and is listed.
- the 3 pilot essays from step 1 are not called again.

## step 3: corpus summary, `extract/corpus_summary.md`

- essays done / bad_json / cli_error (with numbers).
- totals: entities by type, links by kind with the **share of `associated_with`**, drops by reason with the **share of all proposed links**, unlinked person/work (count + the 20 most common names).
- per essay one row: entities, links, drops, unlinked, run time.
- the 10 essays with the highest drop rate, and the 10 with the most `associated_with`.
- **5 random essays for reading by eye**: fixed seed, printed in the summary with links to their review.md. not the 3 pilot essays.

## thresholds (shown in the summary as pass/fail)

- drops < 5% of proposed links.
- 0 bad_json after the one retry.
- `associated_with` < ~30% of links.

a miss doesn't block the report. it's a signal for plan and the user.

## verification

- tests green. the run exits 0 (or stops cleanly on a limit, in which case resume until done).
- 188 extraction json files under `extract/sonnet/` (plus the bad_json ones listed).
- no key in any file or log.
- report to plan: hashes, tests, the summary's totals and thresholds, the 5 random essays. plan reads those 5 review files before telling the user.

## out of scope

merging names (task 04), sqlite, the graph ui, q&a, the api/batch backend, any prompt change beyond step 1.

## step 1 result (plan, 2026-11-11)

`b86b97e`, 58 tests. `associated_with` 60% → 9% (3 of 33), 0 drops, 0 unlinked, 0 bad_json. G'azzoliy/Popper are now `inspired_by`. go for step 2.

known weakness, accepted with no prompt change: a handful of forced kinds are wrong instead of vague. `Pol Getti example_of` should be counterexample. `Kasbiy rivojlanish`/`ego counterexample_of shaxsiy rivojlanish` is really a distinction or an obstacle, not an opposite. the 5 random essays from step 3 will show how often this happens.
