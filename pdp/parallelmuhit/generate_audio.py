#!/usr/bin/env python3
"""
Batch Uzbek TTS audio generation for parallelmuhit.uz essays.

Fetches essay text from the API, synthesises each with the author's cloned voice
using the Uzbek Chatterbox fine-tune, and saves WAV files to ./audio/.

Usage:
    TOKEN=<jwt> python3 generate_audio.py
    TOKEN=<jwt> python3 generate_audio.py --only 166
    TOKEN=<jwt> python3 generate_audio.py --range 160-170
    python3 generate_audio.py --token <jwt> --device cpu
"""

import argparse
import asyncio
import os
import re
import sys
import html as html_module
from html.parser import HTMLParser
from pathlib import Path

import httpx
import numpy as np
import soundfile as sf
import torch

# ---------------------------------------------------------------------------
# Paths (relative to this script's directory = project root)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent
CHATTERBOX_DIR = ROOT / "chatterbox-finetuning"
REFERENCE_WAV = ROOT / "voice_sample" / "reference.wav"
OUTPUT_DIR = ROOT / "audio"

BASE_MODEL_DIR = CHATTERBOX_DIR / "pretrained_models"
MERGED_WEIGHTS = CHATTERBOX_DIR / "uzbek_chatterbox" / "t3_finetuned_merged.safetensors"

API_BASE = "https://b.parallelmuhit.uz"

# ---------------------------------------------------------------------------
# Add chatterbox src to path
# ---------------------------------------------------------------------------
sys.path.insert(0, str(CHATTERBOX_DIR))


# ---------------------------------------------------------------------------
# HTML → plain text
# ---------------------------------------------------------------------------
class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts = []
        self._block_tags = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6",
                            "blockquote", "tr", "td", "th"}

    def handle_starttag(self, tag, attrs):
        if tag in self._block_tags:
            self._parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self._block_tags:
            self._parts.append("\n")

    def handle_data(self, data):
        self._parts.append(data)

    def get_text(self):
        text = "".join(self._parts)
        text = html_module.unescape(text)
        # Collapse multiple blank lines to at most two
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


def html_to_text(html: str) -> str:
    extractor = _TextExtractor()
    extractor.feed(html)
    return extractor.get_text()


# ---------------------------------------------------------------------------
# Model loading (done once)
# ---------------------------------------------------------------------------
_engine = None

def get_engine(device: str):
    global _engine
    if _engine is None:
        from src.chatterbox_.tts import ChatterboxTTS
        from src.chatterbox_.models.t3.t3 import T3
        from safetensors.torch import load_file

        NEW_VOCAB_SIZE = 2454

        print(f"Loading Chatterbox base model from {BASE_MODEL_DIR} ...")
        engine = ChatterboxTTS.from_local(str(BASE_MODEL_DIR), device="cpu")
        t3_config = engine.t3.hp
        t3_config.text_tokens_dict_size = NEW_VOCAB_SIZE

        new_t3 = T3(hp=t3_config)
        print(f"Loading Uzbek fine-tuned weights from {MERGED_WEIGHTS} ...")
        state = load_file(str(MERGED_WEIGHTS))
        missing, unexpected = new_t3.load_state_dict(state, strict=False)
        if missing:
            raise RuntimeError(f"Merged weights failed to load, missing keys: {missing[:5]}")

        engine.t3 = new_t3
        engine.t3.to(device).eval()
        engine.s3gen.to(device).eval()
        engine.ve.to(device).eval()
        engine.device = device
        _engine = engine
        print("Model ready.\n")
    return _engine


# ---------------------------------------------------------------------------
# Synthesis helpers (mirrored from inference_uzbek.py)
# ---------------------------------------------------------------------------
import random


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def _pack(parts, max_chars, sep=" "):
    chunks, cur = [], ""
    for p in parts:
        if not p:
            continue
        candidate = (cur + sep + p).strip() if cur else p
        if len(candidate) <= max_chars:
            cur = candidate
        else:
            if cur:
                chunks.append(cur)
            cur = p
    if cur:
        chunks.append(cur)
    return chunks


def split_sentences(text, max_chars=140):
    text = text.strip()
    if not text:
        return [text]
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        if len(sent) <= max_chars:
            chunks.append(sent)
            continue
        comma_parts = re.split(r'(?<=,)\s+', sent)
        for part in _pack(comma_parts, max_chars):
            if len(part) <= max_chars:
                chunks.append(part)
            else:
                chunks.extend(_pack(part.split(), max_chars))
    return chunks or [text]


def synthesize_text(engine, text: str, seed: int = 42,
                    exaggeration=0.5, cfg_weight=0.5,
                    repetition_penalty=2.0, temperature=0.8):
    from src.utils import trim_silence_with_vad

    chunks = split_sentences(text)
    sr = engine.sr
    silence_gap = np.zeros(int(0.15 * sr), dtype=np.float32)
    pieces = []

    total = len(chunks)
    for i, chunk in enumerate(chunks):
        print(f"  chunk {i+1}/{total}: {chunk[:60]}{'...' if len(chunk) > 60 else ''}")
        set_seed(seed + i)
        with torch.no_grad():
            wav = engine.generate(
                text=chunk,
                audio_prompt_path=str(REFERENCE_WAV),
                exaggeration=exaggeration,
                cfg_weight=cfg_weight,
                repetition_penalty=repetition_penalty,
                temperature=temperature,
            )
        if isinstance(wav, tuple):
            wav = wav[0]
        wav_np = wav.squeeze().cpu().numpy()
        trimmed = trim_silence_with_vad(wav_np, sr)
        pieces.append(trimmed.astype(np.float32))
        pieces.append(silence_gap)

    full_audio = np.concatenate(pieces[:-1]) if pieces else np.zeros(1, dtype=np.float32)
    return full_audio, sr


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------
async def fetch_essays(token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "token": token,
        "Origin": "https://parallelmuhit.uz",
        "Referer": "https://parallelmuhit.uz/",
    }
    async with httpx.AsyncClient(headers=headers, timeout=30) as client:
        resp = await client.get(f"{API_BASE}/blog")
        resp.raise_for_status()
        raw = resp.json()

    essays = [
        {**e, "site_number": i + 1}
        for i, e in enumerate(sorted(raw, key=lambda e: e["createdAt"]), start=1)
    ]
    return essays


async def fetch_content(token: str, slug: str) -> str:
    headers = {
        "Authorization": f"Bearer {token}",
        "token": token,
        "Origin": "https://parallelmuhit.uz",
        "Referer": "https://parallelmuhit.uz/",
    }
    async with httpx.AsyncClient(headers=headers, timeout=30) as client:
        r = await client.get(f"{API_BASE}/blog/slug/{slug}")
        r.raise_for_status()
        return r.json().get("content", "")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def safe_stem(slug: str, number: int) -> str:
    return f"{number:03d}_{slug}"


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--token", default=os.environ.get("TOKEN", ""))
    parser.add_argument("--only", type=int, default=None, metavar="N",
                        help="Process only essay #N")
    parser.add_argument("--range", dest="range_", metavar="A-B",
                        help="Process essays #A through #B (e.g. 160-170)")
    parser.add_argument("--device", default=None,
                        help="cuda / mps / cpu  (auto-detects if omitted)")
    parser.add_argument("--exaggeration", type=float, default=0.5)
    parser.add_argument("--cfg_weight", type=float, default=0.5)
    parser.add_argument("--repetition_penalty", type=float, default=2.0)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if not args.token:
        print("Error: provide JWT via --token or TOKEN env var", file=sys.stderr)
        sys.exit(1)

    range_ = None
    if args.range_:
        try:
            a, b = args.range_.split("-")
            range_ = (int(a), int(b))
        except ValueError:
            print("Error: --range must be A-B (e.g. 160-170)", file=sys.stderr)
            sys.exit(1)

    # Pick device
    if args.device:
        device = args.device
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    print(f"Device: {device}")

    # Fetch essay list
    print("Fetching essay list...")
    essays = asyncio.run(fetch_essays(args.token))
    total_api = len(essays)
    print(f"Found {total_api} essays")

    # Filter
    if args.only is not None:
        essays = [e for e in essays if e["site_number"] == args.only]
        if not essays:
            print(f"No essay #{args.only}", file=sys.stderr)
            sys.exit(1)
    elif range_:
        start, end = range_
        essays = [e for e in essays if start <= e["site_number"] <= end]
        if not essays:
            print(f"No essays in range {start}-{end}", file=sys.stderr)
            sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load model once
    engine = get_engine(device)

    # Process
    for idx, essay in enumerate(essays, 1):
        num = essay["site_number"]
        slug = essay["slug"]
        title = essay.get("title", slug)
        stem = safe_stem(slug, num)
        out_path = OUTPUT_DIR / f"{stem}.wav"

        if out_path.exists():
            print(f"[{idx}/{len(essays)}] skip  #{num} {slug}")
            continue

        print(f"\n[{idx}/{len(essays)}] #{num} {title[:60]}")
        print(f"  → {out_path.name}")

        try:
            html_content = asyncio.run(fetch_content(args.token, slug))
            text = html_to_text(html_content)
            if not text:
                print("  WARNING: empty content, skipping")
                continue

            print(f"  {len(text)} chars plain text")

            audio, sr = synthesize_text(
                engine, text,
                seed=args.seed,
                exaggeration=args.exaggeration,
                cfg_weight=args.cfg_weight,
                repetition_penalty=args.repetition_penalty,
                temperature=args.temperature,
            )
            sf.write(str(out_path), audio, sr)
            duration = len(audio) / sr
            print(f"  Saved: {out_path.name} ({duration:.1f}s)")

        except Exception as exc:
            print(f"  ERROR: {exc}")
            continue

    print("\nDone.")


if __name__ == "__main__":
    main()
