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

## next: task 04 merge names (ready to hand off)

- spec: `TASK_04_merge_names.md`.
- 2026-11-12, user answers: (1) worktree. (2) cherry-pick to main.
- done: `caf3878` is on main as `04a8261` (only Program.cs was committed, and main's other staged files were left staged). feat/pm-kb was reset to `84344e7`. the stash "WIP on feat/pm-kb" still points to caf3878.
- impl works in `/Users/azam_turgunboev/coding-vault-pmkb` (worktree on feat/pm-kb). `pdp/parallelmuhit` and `products/parallelmuhit-kb/extract` there are symlinks to the main checkout, and both are listed in `.git/info/exclude` (patterns that end in `/` don't match symlinks).
- STATUS.md and TASK_04 live in the worktree for real. the main checkout has symlinks to them. impl commits them with task 04.
- next: send impl a pointer to `TASK_04_merge_names.md` (summary + "don't" list, notify_when_idle), with the worktree path as its cwd.
