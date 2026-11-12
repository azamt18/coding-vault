"""Tests for essay_text.md_to_speech_text."""

from pathlib import Path

from essay_text import md_to_speech_text

HERE = Path(__file__).parent

SAMPLE = """---
number: 1
title: Sinov
---

# Sinov insho

*13.08.26*

Birinchi **qalin** va _qiya_ so'z, `kod` ham.



> Iqtibos [havola matni](https://t.me/x/1) bilan.

![](https://example.com/rasm.jpg)

- birinchi band
* ikkinchi band
1. raqamli band

## Kichik sarlavha

Oxirgi gap.
"""

EXPECTED = """Sinov insho

Birinchi qalin va qiya so'z, kod ham.

Iqtibos havola matni bilan.

birinchi band
ikkinchi band
raqamli band

Kichik sarlavha

Oxirgi gap."""


def test_inline_sample():
    assert md_to_speech_text(SAMPLE) == EXPECTED


def test_keeps_tutuq_belgisi_and_inline_dash():
    assert md_to_speech_text("*-Savol bor-mi? O'g'il.*") == "-Savol bor-mi? O'g'il."


def test_committed_171_sample_matches_function():
    md = (HERE / "../../pdp/parallelmuhit/essays_md/171_sharaf.md").resolve()
    txt = HERE / "samples" / "171_sharaf.txt"
    if not md.exists():  # essays_md is gitignored; only check where the corpus exists
        return
    assert txt.read_text(encoding="utf-8") == md_to_speech_text(md.read_text(encoding="utf-8")) + "\n"
