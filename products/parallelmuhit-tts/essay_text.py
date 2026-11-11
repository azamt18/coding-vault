"""Read-aloud text from an essay markdown file (essays_md/*.md).

Same rules as the cost estimate (tts-cost.md, docs/plan-tts.md 1b):
title plus body; no front matter or date line; images dropped, links keep their text;
leading #, > and list markers removed; *, _ and backticks removed; 3+ newlines become 2.
"""

import re

_FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
_DATE_LINE = re.compile(r"^\*\d{2}\.\d{2}\.\d{2}\*[ \t]*$", re.M)
_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_HEADING = re.compile(r"^[ \t]*#+[ \t]*", re.M)
_QUOTE = re.compile(r"^[ \t]*(?:>[ \t]?)+", re.M)
_LIST = re.compile(r"^[ \t]*(?:[-*+]|\d+\.)[ \t]+", re.M)
_EMPHASIS = re.compile(r"[*_`]")
_BLANKS = re.compile(r"\n{3,}")


def md_to_speech_text(md: str) -> str:
    text = md.replace("\r\n", "\n")
    text = _FRONT_MATTER.sub("", text)
    text = _DATE_LINE.sub("", text)
    text = _IMAGE.sub("", text)
    text = _LINK.sub(r"\1", text)
    text = _HEADING.sub("", text)
    text = _QUOTE.sub("", text)
    text = _LIST.sub("", text)  # before _EMPHASIS, so "* item" is seen as a list marker
    text = _EMPHASIS.sub("", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.M)
    text = _BLANKS.sub("\n\n", text)
    return text.strip()


if __name__ == "__main__":
    import sys
    from pathlib import Path

    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.write_text(md_to_speech_text(src.read_text(encoding="utf-8")) + "\n", encoding="utf-8")
    print(f"{dst}: {len(dst.read_text(encoding='utf-8').rstrip(chr(10)))} chars")
