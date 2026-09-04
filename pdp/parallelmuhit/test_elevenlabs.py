#!/usr/bin/env python3
"""
Test ElevenLabs TTS on one essay using a default preset voice.

Usage:
    ELEVEN_KEY=<api_key> TOKEN=<jwt> python3 test_elevenlabs.py --number 171
    python3 test_elevenlabs.py --number 171 --eleven-key <key> --token <jwt>
"""

import argparse
import html
import os
import re
import sys

import httpx
from elevenlabs.client import ElevenLabs


API_BASE = "https://b.parallelmuhit.uz"

# Good Uzbek-compatible voices to try (multilingual models)
# Run with --list-voices to see all available voices
DEFAULT_VOICE = "Aria"   # ElevenLabs multilingual voice


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def fetch_essay(token: str, number: int) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "token": token,
        "Origin": "https://parallelmuhit.uz",
        "Referer": "https://parallelmuhit.uz/",
    }
    with httpx.Client(headers=headers, timeout=30) as client:
        resp = client.get(f"{API_BASE}/blog")
        resp.raise_for_status()
        raw = resp.json()

    essays = sorted(raw, key=lambda e: e["createdAt"])
    essays = [{**e, "site_number": i + 1} for i, e in enumerate(essays, start=1)]

    matched = [e for e in essays if e["site_number"] == number]
    if not matched:
        print(f"Error: no essay #{number}", file=sys.stderr)
        sys.exit(1)
    essay = matched[0]

    with httpx.Client(headers=headers, timeout=30) as client:
        r = client.get(f"{API_BASE}/blog/slug/{essay['slug']}")
        r.raise_for_status()
        essay["content"] = r.json().get("content", "")

    return essay


def list_voices(client: ElevenLabs):
    voices = client.voices.get_all()
    print(f"\n{'Name':<30} {'Voice ID':<25} {'Category'}")
    print("-" * 70)
    for v in voices.voices:
        print(f"{v.name:<30} {v.voice_id:<25} {v.category}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--number", type=int, default=171, metavar="N", help="Essay number to test")
    parser.add_argument("--token", default=os.environ.get("TOKEN", ""), help="JWT auth token")
    parser.add_argument("--eleven-key", default=os.environ.get("ELEVEN_KEY", ""), help="ElevenLabs API key")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Voice name or ID")
    parser.add_argument("--list-voices", action="store_true", help="List available voices and exit")
    args = parser.parse_args()

    if not args.eleven_key:
        print("Error: provide ElevenLabs API key via --eleven-key or ELEVEN_KEY env var", file=sys.stderr)
        sys.exit(1)

    client = ElevenLabs(api_key=args.eleven_key)

    if args.list_voices:
        list_voices(client)
        return

    if not args.token:
        print("Error: provide JWT token via --token or TOKEN env var", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching essay #{args.number}...")
    essay = fetch_essay(args.token, args.number)
    title = essay.get("title", essay["slug"])
    raw_content = essay.get("content", "")
    text = f"{title}\n\n{strip_html(raw_content)}"

    print(f"Title:     {title}")
    print(f"Text len:  {len(text)} chars")
    print(f"Voice:     {args.voice}")
    print(f"Generating audio...")

    audio = client.text_to_speech.convert(
        voice_id=args.voice,
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    out_path = f"audio/test_elevenlabs_{essay['slug']}.mp3"
    os.makedirs("audio", exist_ok=True)
    with open(out_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
