# parallelmuhit kb: status

updated 2026-11-12 (question box checked live) by "Parallel muhit KB on RAG (plan)". this file is the plan session's memory. the details are in the TASK_*.md files.

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

## done, task 07 keep urls (impl, 2026-11-12)

- `extract.parse_essay` returns `links` per paragraph; offline `add_urls.py` patches `extract/sonnet/*.json` paragraphs and adds `urls` to `graph.json` and `graph_grouped.json` (rerun byte-identical, no `claude -p`). run it after any rerun of merge_names/group_ideas.
- ui: node panel shows `↗ anchor` links under quotes and a "links in the essays" list on nodes. 121 python, 26 npm tests, build ok.
- numbers: the "2239" in TASK_07 counted images too (`](` = 2241 = 1742 links + 499 images). 1740 http links, 1732 after per-paragraph dedupe (8 empty anchors/duplicates). (essay, url) pairs 1720: 1090 attached, 630 left out (anchor in no quote and no node name). graph_grouped: 1687 links and 74 nodes carry `urls`.
- 003_javoblar p13 Aziz Rahimov → Shahboz Dolimov carries the youtube url (checked in the json, not in the browser).

- verified by plan 2026-11-12: `e6bd043`, 121 python + 26 npm tests pass, `add_urls.py` rerun byte-identical, 1687 links and 74 nodes carry `urls`. not checked: the youtube url in the browser, how the new panel looks.

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

## done, task 06 graph ui: `f6e2394` (checked by plan 2026-11-12)

- `ui/` (vite + sigma 3.0.3 + forceatlas2). 23 npm tests, build ok, 114 python tests.
- default view: 1773 nodes (1961 − 188 essays), 2186 links = 2193 relation − 76 extracted `wrote` + 69 in_theme. checked by plan.
- `filters.ts`: a link is hidden only by kind, endpoint type or essay. weak links stay visible. this is tested.
- impl's deviations, accepted: sigma 3 (4.x changed the reducer api), node size capped at 16, in_theme hidden under an essay filter, a click on empty space clears the focus, the panel lists all of a node's links, forceatlas2 runs 8 s on load.
- not checked: how it looks. the user opens `npm run dev` in `ui/` and judges the layout, the essay+kind filter on an essay with example_of links, and the camera animation.

## found by the user after the ui review (2026-11-12)

- urls inside essay text are lost in the extraction/graph layer (`plain_text` keeps only the anchor text). the markdown export has them. fix = `TASK_07_keep_urls.md`, offline, no model calls.
- user answers: ui review points 1 and 3 "yes", point 2 unclear (asked again: limit panel links to 10 per kind + "show all"? default: leave as is).
- then `TASK_08_rag_qa.md`: bm25 + graph retrieval, `claude -p` answers with checked citations, cli first.

## decisions, task 08 (user: "yes" to both, 2026-11-12)

- retrieval = bm25 + graph, no embeddings (add only if the eval shows misses).
- cli `ask.py` first, ui question box (needs a local python server) as a later separate task.
- task 07 first, so answers can cite urls.

## open questions

- panel link list: limit to 10 per kind or leave as is (unanswered, default leave).
- eval for task 08: the user writes 6 questions with expected essays.

## done, task 08 cli part: `61562d1` (checked by plan 2026-11-12)

- `retrieve.py` (bm25 over about 6k paragraphs + 1-hop graph links, caps 12 + 20) and `ask.py` (`claude -p` sonnet, citation check, `--context` = no model call). 138 tests.
- checked: the 4 rules from design point 3 are tested (fake id, an id outside the context, quotes copied by code, not found isn't flagged). `--context` on the 2 example questions: Taleb retrieves well with some noise. the book question is weak (generic "tavsiya" paragraphs, no recommends links).
- plan's decision for the eval round: first measure the baseline on the 12 questions. then add a kind-aware step (question words → link kind, e.g. tavsiya → recommends, tanqid → criticises, ilhom → inspired_by, pulling those links ranked by bm25) and measure again.

## done, task 08 rag q&a cli: `61562d1` (impl, checked by plan 2026-11-12)

- `retrieve.py` (bm25 + graph) and `ask.py` (`claude -p` answers, cited paragraph ids verified against the context, quotes and urls copied from the data). 138 python tests pass. `ask.py --context` on a taleb question returns sensible paragraphs from several essays.
- not checked: a live answer (needs the subscription), the graph relations section of the context.

## live ask.py run (2026-11-12, impl)

- question: "Aziz Rahimov Talebning qaysi g'oyalarini tanqid qiladi yoki tavsiya qiladi?" works end to end. 11 cited ids, all printed with copied quotes and urls, none dropped.
- good: the answer is in uzbek and every claim has a paragraph id; the quotes support the claims (004_kitob, 125_oqqush, 140_royxat, 062_xohish, 137_soddavoy).
- weak: the "tanqid" line is clumsy (says "not found", then cites 020_kasb#p10, which is Taleb's own advice). 136_ajratish#p32 and 018_tirbandlik#p11 are Taleb's ideas, not Aziz recommending them, yet they sit under "tavsiya". the model mixes "Aziz recommends" with "Aziz quotes Taleb". a kind-aware step (plan's decision) should help; so could a prompt rule to separate "recommends" from "quotes".
- not judged by the user yet.

## done 2026-11-12 (plan, after "all of them"), commit `e9c4d32`

- overrides applied: 4 idea merges (hikmat+hikmat egasi, Mimesis+mimetik qaramlik, Status+Status o'yinlari, kutilma+Kichik kutuvlar) and Umar+Umar hazratlari. ideas 70 → 65. group_ideas had to call the model again (theme cache keyed on the idea set): 13 themes now (was 14), they differ from before. offline rerun byte-identical, 138 tests pass. not done: labels "Charli Manger", "Baffet", "Andryu Gryu" (spelling not given, there is also a separate person "Charlie").
- ask.py prompt rule: "Aziz recommends/criticises" only with his own judgement, otherwise "Aziz X ning fikrini keltiradi"; a missing part says not found. live Taleb question rechecked: the three groups are now separate, no fake "tanqid". still not judged by the user.
- rebase: dry run in a throwaway worktree. feat/pm-kb = feat/savolbor tip `c53d012` + 28 commits, so `git rebase --onto main feat/savolbor` replays only those 28 (no savolbor files, 0 conflicts, 138 tests pass). the real rebase is NOT done, waiting for the user's ok (the tts session also commits here).
- `TASK_09_ui_question_box.md` drafted (the user's ok not recorded here, impl built it anyway, see below).

## done, task 09 ui question box: `234096a` + `b5b14cd` (checked by plan 2026-11-12)

- `serve.py` (stdlib `ThreadingHTTPServer`, 127.0.0.1:8787): `GET /api/health`, `POST /api/ask`; a lock runs one model call at a time; empty/bad json/too long → 400 without a model call, model error → 502 with a one-line message. vite proxies `/api`; the box hides itself when health fails. ui: `answer.ts` renders the answer, dropped citations get a warning, a citation focuses the node.
- checked: 149 python + 33 npm tests pass, `npm run build` ok, code matches design points 1–5 (read `serve.py`, test names, `vite.config.ts`).
- not checked: a live question through `serve.py` + `npm run dev`, a click on a citation in the browser, how the box looks. the user does this.
- STATUS.md was stale before this entry (it said task 09 was only drafted).

## done, pr (2026-11-12)

- force push of the rebased `feat/pm-kb` was blocked by the permission classifier, so the branch went out as `origin/feat/pm-kb-pr` (no force). pr #1 into main, label `enhancement`: https://github.com/azamt18/coding-vault/pull/1. it also carries the tts session's files.
- old `origin/feat/pm-kb` still has the pre-rebase history (its one extra commit `caf3878` equals main's `04a8261`). delete it on github after the merge, and the local tag `pm-kb-before-rebase`.

## live check of the question box (2026-11-12, user)

- ran `serve.py` (8787) + vite on 5174 (the vite on 5173 was started before the `/api` proxy was added, so its box stayed hidden: restart vite after config changes). the user: "looks good for now". no defects reported.
- pr #1 is NOT merged yet (the user did not say merge).

## merged (2026-11-12, user: "merge pr #1", "clean up")

- pr #1 merged into main as `e8626a7` (merge commit, ci green). deleted `origin/feat/pm-kb`, `origin/feat/pm-kb-pr` and the tag `pm-kb-before-rebase`. the local `feat/pm-kb` worktree (`coding-vault-pmkb`) still exists and has one unpushed docs commit (this file).

## next task

- start new work from main (new branch), no task chosen yet. candidates: label spellings "Charli Manger", "Baffet", "Andryu Gryu"; eval round for task 08 (8 draft questions in `eval_questions.json`, kind-aware retrieval step).
