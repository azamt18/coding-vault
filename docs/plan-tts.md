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
| 2. batch path in generate_audio.py | not planned; depends on section 1 sounding good |

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

### verdict

(empty)
