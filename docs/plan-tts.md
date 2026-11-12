# parallelmuhit-tts plan

goal: readable uzbek audio of parallelmuhit.uz essays. earlier attempts gave bad results:
`eleven_multilingual_v2` with preset voice "Aria" (`audio/test_elevenlabs_sharaf.mp3`) and the
chatterbox uzbek fine-tune (`generate_audio.py`). eleven v4 (`eleven_v4`) lists uzbek (`uz`)
and supports instant voice cloning, so try it next.

sources: https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4 ,
https://elevenlabs.io/docs/overview/models

## status

| section | state |
|---|---|
| 1. eleven v4 spike on one paragraph | open |
| 1b. one full essay with the author's clone | open |
| 2. batch path for all essays | not planned; waits on 1b and the user's budget choice |

---

## 1. eleven v4 spike on one paragraph

decided with the user (2026-11-11): test on **one short paragraph**, not a whole essay (old
results were bad, so spend few credits). compare **two voices**: a preset voice and an instant
clone from `voice_sample/reference.wav`. the user picked the clone a/b. the clone uses the
author's voice from a podcast; the user is responsible for consent (elevenlabs asks for it
when you create a clone).

### input

- text: the paragraph from `pdp/parallelmuhit/essays_md/171_sharaf.md` that starts
  "Zamonaviy dunyoda qanday qilib…" (~350 chars). it has `o'`, `g'` and the `'` tutuq belgisi,
  which is the pronunciation we care about.
- commit it as plain text at `products/parallelmuhit-tts/samples/sharaf_p1.txt`, copied exactly
  (keep the ascii `'` as in the source). no api fetch and no jwt are needed.

### what to build

`products/parallelmuhit-tts/try_eleven_v4.py`, a small cli:

- `--text-file` (default `samples/sharaf_p1.txt`)
- `--voice <name or id>`: use a preset voice. default: a multilingual preset from the account,
  e.g. "Aria", so it matches the old v2 test
- `--clone`: use an instant voice clone made from `voice_sample/reference.wav`. create it once
  and save the voice id to `.eleven_voice_id`, which is gitignored. reuse it on later runs so
  each run does not create a new clone
- `--model` (default `eleven_v4`), and always send `language_code="uz"`
- writes `audio/v4_<preset|clone>_sharaf_p1.mp3` (`mp3_44100_128`)
- api key only from the `ELEVEN_KEY` env var. never in args, files or commits.

check against elevenlabs sdk 2.65.0 (installed): the name of the ivc create call and whether
`text_to_speech.convert` takes `language_code`. if a call differs from this plan, use the real
one and note it in "as built".

### tests

`products/parallelmuhit-tts/test_try_eleven_v4.py`, pytest, with the elevenlabs client mocked
(no network):
- convert is called with `model_id="eleven_v4"`, `language_code="uz"` and the text from the file
- `--clone` with no `.eleven_voice_id` creates a clone once and saves the id. with the file
  present, it reuses the id and does not create a clone
- output path naming for preset and clone
- missing `ELEVEN_KEY` exits non-zero with a clear message

### not in scope

- do not call the real elevenlabs api. it spends the user's credits; the user runs it.
- do not change `test_elevenlabs.py` or `generate_audio.py`.
- do not commit any mp3, the key or `.eleven_voice_id`.
- no chunking. one paragraph fits in one request.

### done when

- pytest passes for tts and kb (kb still 14 passed)
- the user runs both commands and listens:
  `ELEVEN_KEY=… python3 try_eleven_v4.py` and `ELEVEN_KEY=… python3 try_eleven_v4.py --clone`
- the user's verdict goes below. it decides whether section 2 happens.

### as built

- sdk 2.65.0 matches the plan: clone is `client.voices.ivc.create(name=..., files=[...])`
  (returns `.voice_id`), and `client.text_to_speech.convert` takes `language_code`.
- `--voice` resolves a name via `client.voices.get_all()` (case-insensitive) to its voice id;
  a value that matches no name is sent as an id. (the old `test_elevenlabs.py` sent the name
  as `voice_id` directly.) `--voice` and `--clone` are mutually exclusive.
- output name is `audio/v4_<voice slug|clone>_<text file stem>.mp3`, e.g.
  `v4_aria_sharaf_p1.mp3`. extra flags for tests/reuse: `--reference`, `--voice-id-file`,
  `--audio-dir`.
- missing `ELEVEN_KEY` prints an error to stderr and exits 2.
- new `products/parallelmuhit-tts/.gitignore`: `.eleven_voice_id`, `audio/v4_*.mp3`.
  (older mp3/wav files in `audio/` were already tracked; left as is.)
- clone name on the account: `parallelmuhit-author-ivc`.
- verified by plan (2026-11-11), commit e48b982: 40 passed (7 tts + 33 kb). kb grew from 14 to
  33 because of kb's own commit 7cf49aa, not this work. `samples/sharaf_p1.txt` is
  byte-identical to line 23 of `171_sharaf.md`. sdk signatures checked. `reference.wav` is 45 s
  mono 22 kHz, under the 1–2 min elevenlabs suggests for ivc, so clone quality may suffer.
- first real run (2026-11-11, by plan with the user's key, at the user's request):
  - account is on the **free** tier: 10,000 chars/month, and `can_use_instant_voice_cloning` is false.
  - "Aria" is not on the account (no such voice → 404 `voice_not_found`). preset names now carry
    a suffix, e.g. "George - Warm, Captivating Storyteller", so an exact name match never finds
    them. the preset run used George by id, `JBFqnCBsd6RMkjVDRZzb`, and wrote
    `audio/v4_jbfqncbsd6rmkjvdrzzb_sharaf_p1.mp3` (339 KB, 309 chars).
  - `--clone` → http 400, `paid_plan_required` / `can_not_use_instant_voice_cloning`. ivc needs a paid plan, so there is no clone sample yet.
  - bugs for impl (small fix):
    1. the output file is opened before the lazy `convert` stream raises, so a failed run leaves
       a 0-byte mp3 (`audio/v4_aria_sharaf_p1.mp3`). write to a temp file and rename it at the end.
    2. catch `elevenlabs.core.api_error.ApiError` and print `body.detail.message`, not a traceback.
    3. match a name by prefix before " - ", and change the default to an existing preset
       (George) instead of Aria. the output label should be the short name ("george"), not the id.
- fix commit 8b81f26, verified by plan: 55 passed (13 tts + 42 kb). against the live api
  (free calls only): `--clone` prints one error line, exits 1, and leaves no `.eleven_voice_id`
  and no partial file. "George", "george" and the id all resolve to George.

### verdict

2026-11-11, user: **sounds good.** the user upgraded to the starter plan, where ivc is enabled,
and generated `audio/stress_ivc_s50_sim75_v4.mp3` (plus a `(1)` copy) themselves: an instant
clone, stability 50, similarity 75, eleven_v4. section 2 (batch) can be planned. the cost
estimate is in `products/parallelmuhit-tts/tts-cost.md`: ≈1.84M chars, ≈$147 at the api rate.

---

## 1b. one full essay with the author's clone

decided with the user (2026-11-11): convert **one full essay** before choosing a budget.

- essay: #171 `sharaf` "Sharaf haqida", 6,648 chars. that's one request (under v4's 10k), and
  the same essay as the paragraph test.
- voice: the user's own clone on the account, "Aziz Rahimov", `GSSGNagQ0qBLqvmOD9Hl`
  (category cloned, made in the elevenlabs ui). use it by id with `--voice`, not `--clone`, which
  would create a second clone. its stored settings are empty (`None`), so the settings must be sent.
- settings the user liked: stability 50, similarity 75 → `voice_settings` with
  `stability=0.5, similarity_boost=0.75`.
- also measure: the account's `character_count` before and after (751 / 40,000 before). that
  settles the open "credits per v4 character" question in `products/parallelmuhit-tts/tts-cost.md`.

### what to build (impl)

- `try_eleven_v4.py`: add `--stability` and `--similarity` (floats from 0 to 1). when either is
  given, pass `voice_settings=VoiceSettings(stability=..., similarity_boost=...)` to convert; when
  neither is, send nothing (as now). mocked tests for both cases.
- `samples/171_sharaf.txt`: the read-aloud text of `pdp/parallelmuhit/essays_md/171_sharaf.md`,
  using the same rules as the cost estimate:
  - title plus body
  - no front matter and no date line (`*dd.mm.yy*`)
  - images dropped; links keep their text
  - leading `#`, `>` and list markers removed; `*`, `_` and backticks removed
  - three or more newlines collapsed to two
  - expected length is 6,648 chars (± a few for a trailing newline). write it with a small
    function `md_to_speech_text(md: str) -> str` in a new `essay_text.py`, so section 2 can reuse
    it, and test it on a small inline md sample.
- not in scope: no real api call (plan runs it), no chunking, no change to `generate_audio.py`.

### run (plan, with the user's key)

`python3 try_eleven_v4.py --text-file samples/171_sharaf.txt --voice GSSGNagQ0qBLqvmOD9Hl --stability 0.5 --similarity 0.75`
→ `audio/v4_aziz-rahimov_171_sharaf.mp3`

### as built

- sdk 2.65.0: `from elevenlabs import VoiceSettings` (same class as `elevenlabs.types.VoiceSettings`).
  fields: stability, similarity_boost, style, use_speaker_boost, speed.
- `--stability` / `--similarity` take a float in 0–1 (anything else is an argparse error, exit 2).
  with only one given, the other stays `None`, and the sdk leaves it out of the request json
  (checked: `{'stability': 0.3}`).
- `essay_text.md_to_speech_text` follows the rules above. list markers are removed before `*`/`_`,
  and trailing spaces are stripped. it also runs as a cli:
  `python3 essay_text.py <md> <txt>` (writes the text plus one trailing newline).
- `samples/171_sharaf.txt`: 6,648 chars (6,649 with the trailing newline), which matches the csv.

### run result (plan, 2026-11-12)

- full essay #171, one request: 417 s of audio, 6.7 MB.
- measured cost: 2,659 credits for 6,648 chars (751 → 3,410), ≈0.40 credits per char. audio is
  ≈1.05 min per 1k chars, as estimated.
- whole catalog: 1.84M chars ≈ 735k credits ≈ 18 months on starter (40k/month, ≈10 essays a month).
- `tts-cost.md` still assumes 1 credit per char. impl must correct it.
- verdict: pending, the user hasn't listened yet.
