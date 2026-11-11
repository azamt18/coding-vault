#!/usr/bin/env python3
"""
Spike: ElevenLabs eleven_v4 Uzbek TTS on one paragraph (docs/plan-tts.md, section 1).

Usage:
    ELEVEN_KEY=<key> python3 try_eleven_v4.py                 # preset voice (George)
    ELEVEN_KEY=<key> python3 try_eleven_v4.py --voice <name|id>
    ELEVEN_KEY=<key> python3 try_eleven_v4.py --clone         # instant clone of reference.wav

The API key is read only from the ELEVEN_KEY env var.
The clone's voice id is cached in .eleven_voice_id (gitignored), so it is created once.
"""

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
DEFAULT_TEXT_FILE = HERE / "samples" / "sharaf_p1.txt"
DEFAULT_REFERENCE = HERE / "voice_sample" / "reference.wav"
DEFAULT_VOICE_ID_FILE = HERE / ".eleven_voice_id"
DEFAULT_AUDIO_DIR = HERE / "audio"
DEFAULT_VOICE = "George"
DEFAULT_MODEL = "eleven_v4"
LANGUAGE_CODE = "uz"
OUTPUT_FORMAT = "mp3_44100_128"
CLONE_NAME = "parallelmuhit-author-ivc"


def make_client(api_key: str):
    from elevenlabs.client import ElevenLabs

    return ElevenLabs(api_key=api_key)


def short_name(name: str) -> str:
    """Premade names look like "George - Warm, Captivating Storyteller"; keep "George"."""
    return name.split(" - ", 1)[0].strip()


def resolve_preset(client, voice: str) -> tuple[str, str]:
    """Return (voice_id, label) for a voice name or id on the account.

    A name matches the full name or its short name (case-insensitive); an id matches
    a voice id. The label is the voice's short name. Anything else is sent as an id
    and used as the label.
    """
    want = voice.lower()
    for v in client.voices.get_all().voices:
        if want in (v.name.lower(), short_name(v.name).lower(), v.voice_id.lower()):
            return v.voice_id, short_name(v.name)
    return voice, voice


def clone_voice_id(client, reference: Path, id_file: Path) -> str:
    if id_file.exists():
        saved = id_file.read_text().strip()
        if saved:
            print(f"Reusing clone {saved} from {id_file.name}")
            return saved
    print(f"Creating instant clone from {reference.name} ...")
    with reference.open("rb") as f:
        resp = client.voices.ivc.create(name=CLONE_NAME, files=[f])
    id_file.write_text(resp.voice_id + "\n")
    print(f"Saved clone id {resp.voice_id} to {id_file.name}")
    return resp.voice_id


def output_path(audio_dir: Path, label: str, text_file: Path) -> Path:
    slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-") or "voice"
    return audio_dir / f"v4_{slug}_{text_file.stem}.mp3"


def api_error_message(err) -> str:
    body = getattr(err, "body", None)
    detail = body.get("detail") if isinstance(body, dict) else None
    if isinstance(detail, dict) and detail.get("message"):
        status = detail.get("status")
        return f"{status}: {detail['message']}" if status else detail["message"]
    if detail:
        return str(detail)
    return str(body or err)


def write_atomically(out: Path, chunks) -> None:
    """Stream chunks to a temp file next to out; rename only after the stream completes."""
    out.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=out.parent, prefix=f".{out.stem}.", suffix=".part")
    try:
        with os.fdopen(fd, "wb") as f:
            for chunk in chunks:
                f.write(chunk)
        os.replace(tmp, out)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def parse_args(argv):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--text-file", type=Path, default=DEFAULT_TEXT_FILE)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--voice", default=DEFAULT_VOICE, help="preset voice name or id")
    g.add_argument("--clone", action="store_true", help="use an instant clone of --reference")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    p.add_argument("--voice-id-file", type=Path, default=DEFAULT_VOICE_ID_FILE)
    p.add_argument("--audio-dir", type=Path, default=DEFAULT_AUDIO_DIR)
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    key = os.environ.get("ELEVEN_KEY")
    if not key:
        print("error: set the ELEVEN_KEY environment variable (the key is never taken from args)", file=sys.stderr)
        sys.exit(2)

    text = args.text_file.read_text(encoding="utf-8").strip()
    client = make_client(key)

    from elevenlabs.core.api_error import ApiError

    try:
        if args.clone:
            voice_id = clone_voice_id(client, args.reference, args.voice_id_file)
            label = "clone"
        else:
            voice_id, label = resolve_preset(client, args.voice)

        out = output_path(args.audio_dir, label, args.text_file)
        print(f"Model {args.model}, language {LANGUAGE_CODE}, voice {label} ({voice_id}), {len(text)} chars")
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id=args.model,
            language_code=LANGUAGE_CODE,
            output_format=OUTPUT_FORMAT,
        )
        write_atomically(out, audio)  # convert is lazy; ApiError can surface mid-stream
    except ApiError as e:
        print(f"error: elevenlabs api ({e.status_code}): {api_error_message(e)}", file=sys.stderr)
        sys.exit(1)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
