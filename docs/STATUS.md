# parallelmuhit-tts — status

updated 2026-11-12 by the plan session. full plan: `docs/plan-tts.md` on branch `feat/pm-kb`.

## working rules (from the user, via managing claude)

- the plan file and this STATUS.md are the memory, not the chat. update this file after every
  decision and every verified hand-off: goal, decisions, done, next step, open questions.
- hand-offs to impl are pointers: plan section name plus a short summary. never paste code,
  logs or diffs.
- avoid screenshots and large tool output. read text, grep, or ask impl for a summary.
- at the end of a planning phase: update this file, then tell the user "safe to /clear, state
  is in STATUS.md".
- after many turns or a lot of output, tell the user to /compact (say what to keep) or /clear,
  at a natural stopping point, never mid-verification.
- all prose in lowercase (code and paths keep their case).

## goal

uzbek audio of the 188 parallelmuhit.uz essays, read in the author's voice.

## decisions

- engine: elevenlabs `eleven_v4`, `language_code="uz"`. the chatterbox fine-tune and
  multilingual_v2 sounded bad.
- voice: the user's clone "Aziz Rahimov", `GSSGNagQ0qBLqvmOD9Hl`, used by id with `--voice`.
  settings: stability 0.5, similarity 0.75. the clone has no stored settings, so they are sent
  on every request.
- account: elevenlabs **starter** plan, 40,000 credits/month. the key stays out of files; the
  user should rotate it after testing (it is in chat history).
- text: `essay_text.md_to_speech_text()`: title plus body, no front matter, no date line, no
  markdown symbols.
- mp3s are not committed (`audio/*.mp3` is gitignored).

## done (all on `feat/pm-kb`, not pushed)

- e48b982: `try_eleven_v4.py`, the one-paragraph spike
- 8b81f26: atomic writes, one-line api errors, matching voices by short name
- 7310aed: cost estimate, `products/parallelmuhit-tts/tts-cost.md` and `tts-cost-per-essay.csv`
- 63fff37: gitignore `audio/*.mp3`
- 90e6268: `--stability`/`--similarity`, `essay_text.py`, `samples/171_sharaf.txt`
  (verified: 20 tts tests pass)
- 2026-11-12, run by plan: **full essay #171** (6,648 chars) → 417 s of audio, 6.7 MB. file:
  `/private/tmp/claude-501/-Users-azam-turgunboev-coding-vault/b98d77b4-2f33-496f-817b-bb1ea07ef49b/scratchpad/tts90e/products/parallelmuhit-tts/out/v4_aziz-rahimov_171_sharaf.mp3`

## measured cost

- essay 171 used **2,659 credits for 6,648 chars, ≈0.40 credits per char** (751 → 3,410).
- audio length is ≈1.05 min per 1k chars, as estimated.
- whole back catalog: 1.84M chars ≈ **735k credits** ≈ 18 months on starter. one average
  essay is ≈3.9k credits, so starter covers ≈10 essays a month.
- `tts-cost.md` still assumes 1 credit per char for plans. it needs this correction (impl, on
  `feat/pm-kb`).

## next step

the user listens to essay 171 and gives a verdict. then the user chooses a budget (bigger plan
vs starter over time) → plan section 2, a batch with skip-existing, a temp-file write and
chunking for the 82 essays over 10k chars.

## open questions / blockers

- 2026-11-12: the user hasn't listened yet. tts is parked while kb task 04 runs. feat/pm-kb is now checked out in the worktree `/Users/azam_turgunboev/coding-vault-pmkb` (tip `84344e7`, the stray dotnet commit is gone), so `docs/plan-tts.md` and the tts files are there.

- **the working tree is on `main`**, switched 2026-11-12 13:19 (a stash "WIP on feat/pm-kb"
  holds dotnet work). the tts files and `docs/plan-tts.md` are not on disk until someone checks
  out `feat/pm-kb` again. the plan session does not switch branches.
- the run result and 0.40 credits/char are now in `plan-tts.md` 1b "run result" (written in the
  worktree, uncommitted; the verdict line there is still pending).
- ~~impl stopped because it hit its usage limit~~ resolved: 1b was finished and reported
  (90e6268). impl is idle with nothing queued (2026-11-12).

## impl (updated by impl, 2026-11-12)

- done: e48b982, 8b81f26, 7310aed, 63fff37, 90e6268. last run: 92 passed (20 tts + 72 kb).
- next impl task: the `tts-cost.md` correction (0.40 credits/char), once plan sends the hand-off.
  work in the worktree `/Users/azam_turgunboev/coding-vault-pmkb`, not in the main checkout.
- decisions made by impl: voice-settings fields left as `None` are dropped from the request
  json; `md_to_speech_text` strips list markers before `*`/`_`.
- open: none from impl.
