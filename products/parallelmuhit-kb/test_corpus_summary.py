"""Tests for corpus_summary.py. Built from recorded raw answers, no model calls."""

import copy
import json
import re

import pytest

import corpus_summary
import extract
from test_extract import ESSAY_MD, FIXTURE


def _write_essay(data, n, slug):
    md = ESSAY_MD.replace("number: 149", f"number: {n}").replace("slug: qiziquvchanlik", f"slug: {slug}")
    (data / "essays_md" / f"{n:03d}_{slug}.md").write_text(md, encoding="utf-8")


def _raw_with(relations=None, drop_relations=False):
    raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
    blk = next(b for b in raw["content"] if b["type"] == "text")
    d = json.loads(blk["text"])
    if relations is not None:
        d["relations"] = relations
    if drop_relations:
        del d["relations"]
    blk["text"] = json.dumps(d, ensure_ascii=False)
    raw["duration_ms"] = 2000
    return raw


@pytest.fixture
def corpus(tmp_path):
    data, out = tmp_path / "data", tmp_path / "extract"
    (data / "essays_md").mkdir(parents=True)
    raw_dir = out / "raw" / "sonnet"
    raw_dir.mkdir(parents=True)
    good = _raw_with()
    for n in [2, 10, 11, 12, 13, 14, 15, 16, 149, 180]:
        slug = f"e{n}"
        _write_essay(data, n, slug)
        (raw_dir / f"{n:03d}_{slug}.json").write_text(json.dumps(good, ensure_ascii=False), encoding="utf-8")
    _write_essay(data, 20, "broken")
    (raw_dir / "020_broken.json").write_text(json.dumps(_raw_with(drop_relations=True)), encoding="utf-8")
    _write_essay(data, 21, "limit")    # no raw answer: the cli failed
    _write_essay(data, 22, "waiting")  # no raw answer: never started
    (out / "last_run.json").write_text(json.dumps({"failures": [
        ["021_limit", "sonnet", "cli_error"], ["022_waiting", "sonnet", "not_started"]]}), encoding="utf-8")
    return data, out


def test_status_counts(corpus):
    data, out = corpus
    s = corpus_summary.collect(data, out)
    assert len(s["done"]) == 10
    assert s["bad_json"] == ["020_broken"]
    assert s["cli_error"] == ["021_limit"]
    assert s["not_started"] == ["022_waiting"]


def test_totals_and_shares(corpus):
    data, out = corpus
    s = corpus_summary.collect(data, out)
    t = s["totals"]
    # per fixture essay: 4 kept relations, 6 dropped relations, entities person 1 / idea 1 / organization 1
    assert t["links"] == 40 and t["proposed"] == 100
    assert t["drops_by_reason"] == {"quote_not_found": 20, "bad_paragraph": 10, "unknown_entity": 20, "bad_kind": 10}
    assert t["drop_share"] == pytest.approx(0.6)
    assert t["kinds"]["associated_with"] == 20 and t["associated_share"] == pytest.approx(0.5)
    assert t["entities"] == {"person": 10, "work": 0, "idea": 10, "organization": 10}


def test_thresholds_pass_fail(corpus):
    data, out = corpus
    md = corpus_summary.render(corpus_summary.collect(data, out))
    assert re.search(r"drops < 5% of proposed links.*FAIL", md)
    assert re.search(r"0 bad_json after the retry.*FAIL", md)
    assert re.search(r"associated_with < 30% of links.*FAIL", md)


def test_thresholds_can_pass(corpus, tmp_path):
    data, out = corpus
    clean = _raw_with(relations=[
        {"source": "Charli Manger", "target": "Qiziquvchanlik", "kind": "recommends", "label": "x",
         "paragraph": "p3", "quote": "sohadan tashqari o'rganish ham muhimligini"}])
    for p in (out / "raw" / "sonnet").glob("*.json"):
        p.write_text(json.dumps(clean, ensure_ascii=False), encoding="utf-8")
    md = corpus_summary.render(corpus_summary.collect(data, out))
    assert re.search(r"drops < 5% of proposed links.*PASS", md)
    assert re.search(r"0 bad_json after the retry.*PASS", md)
    assert re.search(r"associated_with < 30% of links.*PASS", md)


def test_sample_is_fixed_and_skips_pilot(corpus):
    data, out = corpus
    a = corpus_summary.collect(data, out)["sample"]
    b = corpus_summary.collect(data, out)["sample"]
    assert a == b and len(a) == 5
    assert not {"002_e2", "149_e149", "180_e180"} & set(a)


def test_render_sections_and_links(corpus):
    data, out = corpus
    md = corpus_summary.render(corpus_summary.collect(data, out))
    for heading in ("## status", "## totals", "## thresholds", "## per essay", "## highest drop rate",
                    "## most associated_with", "## unlinked person/work", "## 5 random essays to read"):
        assert heading in md
    sample = corpus_summary.collect(data, out)["sample"]
    assert f"[{sample[0]}](sonnet/{sample[0]}.review.md)" in md
    assert "| 010_e10 | 3 | 4 | 6 | 0 | 2.0 s |" in md
    assert "bad_json: 020_broken" in md and "cli_error: 021_limit" in md


def test_unlinked_top_names_by_base_name(corpus):
    data, out = corpus
    clean = _raw_with(relations=[])
    for p in (out / "raw" / "sonnet").glob("*.json"):
        p.write_text(json.dumps(clean, ensure_ascii=False), encoding="utf-8")
    s = corpus_summary.collect(data, out)
    assert s["totals"]["unlinked"] == 11
    assert s["unlinked_top"][0] == ("Charli Manger", 11)


def test_main_writes_last_run(tmp_path, monkeypatch):
    out = tmp_path / "extract"
    monkeypatch.setattr(extract, "run_all", lambda *a, **k: ([], [("021_limit", "sonnet", "cli_error")]))
    monkeypatch.setattr(extract, "select_paths", lambda data_dir, spec: [tmp_path / "021_limit.md"])
    monkeypatch.setattr("sys.argv", ["extract.py", "--essays", "all", "--out-dir", str(out)])
    with pytest.raises(SystemExit):
        extract.main()
    assert json.loads((out / "last_run.json").read_text())["failures"] == [["021_limit", "sonnet", "cli_error"]]
