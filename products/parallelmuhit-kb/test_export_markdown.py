"""Tests for the pure parts of export_markdown.py. No network."""

import re

import yaml

from export_markdown import (
    filename_for,
    frontmatter,
    html_to_markdown,
    number_essays,
    render_essay,
    select_essays,
)


def test_numbering_matches_download_essays():
    raw = [
        {"slug": "c", "createdAt": "2024-03-01"},
        {"slug": "a", "createdAt": "2024-01-01"},
        {"slug": "b", "createdAt": "2024-02-01"},
    ]
    essays = number_essays(raw)
    assert [(e["slug"], e["site_number"]) for e in essays] == [("a", 2), ("b", 3), ("c", 4)]


def test_filename_for():
    assert filename_for({"slug": "daraxt", "site_number": 2}, ".md") == "002_daraxt.md"
    assert filename_for({"slug": "mimetik", "site_number": 180}, ".json") == "180_mimetik.json"


def test_select_number_and_range():
    essays = number_essays([{"slug": s, "createdAt": f"2024-01-0{i}"} for i, s in enumerate("abcd", 1)])
    assert [e["slug"] for e in select_essays(essays, only=3)] == ["b"]
    assert [e["slug"] for e in select_essays(essays, range_=(3, 4))] == ["b", "c"]
    assert len(select_essays(essays)) == 4


def test_paragraphs_separated_by_one_blank_line():
    md = html_to_markdown("<p>Birinchi\nqator.</p><p>Ikkinchi.</p>")
    assert md == "Birinchi qator.\n\nIkkinchi."


def test_blockquote_and_headings():
    md = html_to_markdown("<h2>Bob</h2><blockquote><p>Hikmat.</p></blockquote>")
    assert "## Bob" in md
    assert "> Hikmat." in md


def test_relative_urls_made_absolute():
    md = html_to_markdown('<p><a href="/daraxt">bu</a> <img src="/uploads/x.jpg" alt="rasm"></p>')
    assert "[bu](https://parallelmuhit.uz/daraxt)" in md
    assert "![rasm](https://b.parallelmuhit.uz/uploads/x.jpg)" in md


def test_absolute_urls_unchanged():
    md = html_to_markdown('<p><a href="https://example.com/a">x</a></p>')
    assert "[x](https://example.com/a)" in md


def test_no_html_tags_left():
    md = html_to_markdown('<div><p><span style="color:red">Matn</span><br></p><figure><img src="/a.png"></figure></div>')
    assert not re.search(r"<[a-z]", md)


def test_uzbek_characters_untouched():
    text = "Oʻzbek gʻoyasi, ‘qoʻshtirnoq’ va o'g'il"
    md = html_to_markdown(f"<p>{text}</p>")
    assert md == text


def test_frontmatter_survives_quotes_and_colons():
    meta = {
        "number": 2,
        "slug": "daraxt",
        "title": 'Daraxtlardan "rivojlanish": o\'rganamiz',
        "author": "Alijanov Ibrohim",
        "created_at": "2024-01-01T00:00:00.000Z",
        "source": "https://parallelmuhit.uz/daraxt",
    }
    fm = frontmatter(meta)
    assert fm.startswith("---\n") and fm.endswith("---\n")
    assert yaml.safe_load(fm.strip("-\n")) == meta


def test_render_essay():
    essay = {
        "slug": "daraxt",
        "site_number": 2,
        "title": "Daraxt: oʻsish",
        "author": {"name": "Alijanov Ibrohim"},
        "createdAt": "2024-01-01T00:00:00.000Z",
    }
    out = render_essay(essay, {"content": "<p>Matn.</p>"})
    head, body = out.split("---\n", 2)[1:]
    meta = yaml.safe_load(head)
    assert meta["number"] == 2 and meta["title"] == "Daraxt: oʻsish"
    assert meta["source"] == "https://parallelmuhit.uz/daraxt"
    assert body == "\n# Daraxt: oʻsish\n\nMatn.\n"


# --- data dir: scripts live in products/, essays stay in pdp/parallelmuhit ---

import json
from pathlib import Path

import download_essays
import export_markdown


def test_default_data_dir_is_pdp_parallelmuhit():
    expected = Path(__file__).resolve().parents[2] / "pdp" / "parallelmuhit"
    assert export_markdown.DEFAULT_DATA_DIR == expected
    assert download_essays.DEFAULT_DATA_DIR == expected


def test_data_dir_flag(tmp_path):
    assert export_markdown.parse_args(["--offline"]).data_dir == export_markdown.DEFAULT_DATA_DIR
    assert export_markdown.parse_args(["--offline", "--data-dir", str(tmp_path)]).data_dir == tmp_path
    assert download_essays.parse_args(["--data-dir", str(tmp_path)]).data_dir == tmp_path


def test_offline_export_writes_into_data_dir_not_cwd(tmp_path, monkeypatch):
    data = tmp_path / "data"
    (data / "essays_raw").mkdir(parents=True)
    essay = {"slug": "daraxt", "title": "Daraxt", "author": {"name": "A"}, "createdAt": "2024-01-01"}
    (data / "essays_raw" / "_list.json").write_text(json.dumps([essay]), encoding="utf-8")
    (data / "essays_raw" / "002_daraxt.json").write_text(json.dumps({"content": "<p>Matn.</p>"}), encoding="utf-8")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)

    assert export_markdown.export("", None, None, force=False, offline=True, data_dir=data) == 0
    assert (data / "essays_md" / "002_daraxt.md").read_text(encoding="utf-8").endswith("Matn.\n")
    assert list(elsewhere.iterdir()) == []
