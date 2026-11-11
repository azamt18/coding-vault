# task 02: extraction pilot on 3 essays

goal: find out whether claude can pull a trustworthy graph (people, works, ideas, organizations and the links between them, each link backed by a quote) out of the uzbek essays, and which model to use for the full run. this is step 1 of the knowledge graph. the graph view and q&a come later.

decided with the user on 2026-11-11 (plan session). the "my call" items are plan decisions the user accepted in a summary.

## step 0: fix the author in the frontmatter (its own commit, first)

the api's `author` is the account that posted the essay, not the writer: 179 × Alijanov Ibrohim, 5 × Aziz Rahimov, 2 × Ibrohim, 2 × Нилюфар. all 188 essays are by **Aziz Rahimov**.

- `export_markdown.py`: write the api value as `posted_by:`, and `author: Aziz Rahimov` for every essay (a constant, not from the api).
- test first. then `--offline --force` rebuild of all 188 (no api calls).
- check: 188 × `author: Aziz Rahimov`. `posted_by` gives 179 / 5 / 2 / 2 as above. nothing else in the md files changes: diff against a copy, and only those two lines may differ.

## step 1: `extract.py` in `products/parallelmuhit-kb/`

### input
- `pdp/parallelmuhit/essays_md/NNN_slug.md` (use the same `DEFAULT_DATA_DIR` / `--data-dir` as the export).
- pilot essays: `002_daraxt`, `149_qiziquvchanlik`, `180_mimetik`. flags: `--essays 2,149,180`, `--model haiku|sonnet|both`, `--force`.

### paragraphs
- split the frontmatter on the first two `---` lines only (002 has a `---` rule in the body).
- body blocks are separated by a blank line. skip image-only blocks, horizontal rules and the date line. `# title` and other headings count as paragraphs.
- the text sent to the model and used for quote checks is the block with markdown markup removed: links → their text, `*`/`_` emphasis and `>` removed. apostrophes and uzbek letters stay byte for byte. *(my call: otherwise quotes fail on `*` and link syntax)*
- ids: `p1`, `p2`, … within the essay, and `NNN_slug#pK` globally.

### model call
- claude directly: anthropic python sdk, key only from `ANTHROPIC_API_KEY`, never written anywhere. models `claude-haiku-5-5` and `claude-sonnet-5-5`.
- **read the claude-api skill before writing the api code** (structured outputs, current sdk calls). the claude cookbook knowledge-graph guide uses `client.messages.parse(..., output_format=<pydantic model>)`. follow that if it's still current.
- **one call per essay per model**: title plus numbered paragraphs (`[p1] …`). the prompt is in english. it states that the author is Aziz Rahimov and that "men"/"biz" (I/we) in the author's voice means him.
- save each raw response in `extract/raw/<model>/NNN_slug.json`. if it exists, don't call again unless `--force`.

### what the model returns
- **entities:** `name` (exactly as written in the essay), `type` ∈ `person | work | idea | organization`, `description` (one sentence in uzbek, grounded in the essay), `aliases` (other spellings in this essay), `paragraphs` (ids where it appears).
  - work = book, article, film, podcast, talk. no places or events.
  - only things the essay actually discusses, not every passing word.
- **relations:** `source`, `target` (entity names, or "Aziz Rahimov" for the author), `kind`, `label` (short free phrase in uzbek, the essay's own wording), `paragraph` (id), `quote` (exact text from that paragraph).
  - `kind` ∈ `wrote | recommends | criticises | inspired_by | example_of | associated_with`. *(my call for the starting list. the user adjusts it after reading the pilot.)*
  - direction: `source --kind--> target` (e.g. person wrote work; idea example_of idea).

### checks in code (drop, don't fix)
- quote must be an exact substring of the named paragraph's plain text. drop with reason `quote_not_found` or `bad_paragraph`.
- source/target must be an extracted entity or the author. drop with reason `unknown_entity`.
- `kind`/`type` outside the lists: drop with reason `bad_kind` / `bad_type`.
- no aliases merging, no name cleanup. that's task 03.

### graph pieces built by code, not by the model
- an essay node per essay (number, slug, title, source url from the frontmatter).
- one author node, `Aziz Rahimov`. no url.
- a `mentioned_in` edge from each entity to its essay, with the paragraph ids.

### output, all in `products/parallelmuhit-kb/extract/` (gitignored, like the essays)
- `extract/<model>/NNN_slug.json`: essay, model, paragraphs (id + text), entities, relations, dropped (item + reason), usage (input/output tokens).
- `extract/<model>/NNN_slug.review.md`: for the user to read. entities grouped by type with description and paragraphs. relations as `source —kind (label)→ target`, with the quote and the paragraph id under each. dropped items at the end with their reason.
- `extract/compare.md`: per essay × model, the entity count by type, the relation count by kind, the dropped count by reason, tokens and cost. no quality verdict. the user judges that from the review files.

### tests (no network)
- paragraph split: frontmatter with a body `---` (002), image-only blocks skipped, headings kept, markup stripped while `‘ ʻ '` stay unchanged.
- quote check: exact match passes. any apostrophe variant swapped fails. a wrong paragraph id fails.
- a recorded fake model response → validation, the drop reasons, the essay/author/mentioned_in pieces, and the review md rendering.
- raw response cache: a second run makes no api call.

## verification (before calling it done)
- step 0 checks above.
- run `--essays 2,149,180 --model both`: 6 json + 6 review.md + compare.md, exit 0.
- the key is in no file, log or commit.
- report to plan: hashes, tests, the compare.md table, the drop counts, the total cost. plan reads the 6 review files before telling the user.

## out of scope
merging aliases/entities, sqlite, the graph ui, the other 185 essays, q&a/rag, prompt caching and the batch api (that's for the full run).

## change 2026-11-11: pilot runs on the claude code subscription, not the api

there's no anthropic api key (only openrouter), and the user wants the subscription. the pilot calls `claude -p` as a subprocess instead of the sdk. the sdk version stays for the full run later (batch api).

- a second implementation of the model-call function. paragraphs, checks, review and compare stay as they are.
- `claude -p --model claude-haiku-5-5|claude-sonnet-5-5 --output-format json`. the schema goes in the prompt as a json schema, and the answer is parsed from the result text. invalid json or a schema mismatch is an error for that essay × model (`bad_json`), with no retries that hide it.
- clean environment: remove `ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_BASE` from the subprocess env. otherwise claude code takes the openrouter key instead of the subscription.
- isolation: no tools, no mcp, no user CLAUDE.md, hooks or plugins in the call (pick the matching flags from `claude --help`, such as a system-prompt override, setting sources and a strict mcp config). cwd is an empty temp dir.
- `compare.md`: instead of tokens/cost, run time and `total_cost_usd`/usage from the json output if claude code provides them (marked as "subscription, not billed").
- `--backend cli|sdk`, default `cli`.

## pilot result (plan, 2026-11-11)

code `7cf49aa`, `d5eb2c9`, `86ea7f2`. 42 tests green. run via `claude -p` (subscription), 6 calls, 2 min 57 s.
- 5 of 6 worked. `bad_json` on 149 × haiku: the `relations` key is missing.
- drops: 3 × `quote_not_found`, all caused by U+00A0 (`&nbsp;`) in the essays, which the models copy as a normal space. fix: U+00A0 → space in `plain_text()`.
- sonnet: all link kinds get used, plus author links ("Aziz Rahimov inspired_by Ryan Holiday"). haiku: 002 has 5 of 5 links as `associated_with` with labels like "misol", "mashq".
- haiku found things sonnet missed: GM (002), takasur surasi (180).

plan's read of the 5 review files:
- **quotes anchor the link but don't always prove it**: "George Soros milliarder.", "Charli Mungerning mashhur gapiga qarang".
- **counterexamples end up as `example_of`**: Soros, Pol Getti and NasDaily appear as positive examples, though the essay holds them up as the opposite.
- **names vary**: "Charli Munger" (002) vs "Charli Manger" (149), lowercase "prison break", "Teylor svift", inflected aliases ("janob Talebda", "egosi"). this is task 03's problem, but extraction can help if it gives the base form.

## changes after the pilot (user approved, 2026-11-11)

1. **model for the full run: `claude-sonnet-5-5`.** haiku is dropped, and the rerun is sonnet only.
2. **new kind `counterexample_of`**: the essay holds someone or something up as the opposite of an idea (Soros: money ≠ growth). the list now has 7 kinds.
3. **quote = the whole sentence that states the link itself**, not just the sentence where the name appears. the quote alone must make the link clear. the check stays an exact substring of the paragraph.
4. **`base_name`** on each entity: the name in its basic form with normal capitals ("janob Talebda" → "Taleb", "Teylor svift" → "Teylor Svift"). the essay's spelling and transliteration stay. `name` stays exactly as written. no merging, it's only a hint for task 03.

rerun: 3 essays × sonnet with `--force`. compare against the previous sonnet run: the number of links, how many are `counterexample_of`, the drops.
