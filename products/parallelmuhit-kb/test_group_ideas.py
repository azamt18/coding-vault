"""Tests for group_ideas.py. No model calls: the cli is a fake subprocess."""

import json
import subprocess
from pathlib import Path

import pytest

import extract
import group_ideas as gi

FIXTURES = Path(__file__).parent / "fixtures"


def idea(nid, label, essays, aliases=(), mentions=1):
    return {"id": nid, "label": label, "type": "idea", "aliases": list(aliases),
            "descriptions": {e: f"{label} tavsifi {e}" for e in essays}, "essays": list(essays),
            "mention_count": mentions}


def graph():
    nodes = [
        idea("idea:hasad", "hasad", ["001_a", "002_b", "003_c"], mentions=5),
        idea("idea:kibr", "kibr", ["001_a", "002_b"], aliases=["Kibr"], mentions=2),
        idea("idea:manmanlik", "manmanlik", ["002_b", "004_d"], mentions=3),
        idea("idea:sabr", "Sabr", ["003_c", "004_d"], mentions=2),
        idea("idea:yolgiz", "yolg'iz fikr", ["001_a"]),
        {"id": "person:ali", "label": "Ali", "type": "person", "aliases": [], "descriptions": {},
         "essays": ["001_a"], "mention_count": 1},
        {"id": "essay:002_b", "label": "B", "type": "essay"},
        {"id": "essay:004_d", "label": "D", "type": "essay"},
    ]
    links = [
        {"source": "person:ali", "target": "idea:kibr", "kind": "criticises", "essay": "001_a", "quote": "q1"},
        {"source": "idea:kibr", "target": "idea:manmanlik", "kind": "associated_with", "essay": "002_b", "quote": "q2"},
        {"source": "idea:hasad", "target": "idea:yolgiz", "kind": "example_of", "essay": "001_a", "quote": "q3"},
        {"source": "idea:kibr", "target": "essay:002_b", "kind": "mentioned_in", "essay": "002_b", "paragraphs": ["p3"]},
        {"source": "idea:manmanlik", "target": "essay:002_b", "kind": "mentioned_in", "essay": "002_b",
         "paragraphs": ["p10", "p2"]},
        {"source": "idea:manmanlik", "target": "essay:004_d", "kind": "mentioned_in", "essay": "004_d", "paragraphs": ["p1"]},
    ]
    return {"nodes": nodes, "links": links}


# --- selection ---


def test_select_only_ideas_in_two_or_more_essays():
    selected, rest = gi.select_ideas(graph())
    assert [n["id"] for n in selected] == ["idea:hasad", "idea:kibr", "idea:manmanlik", "idea:sabr"]
    assert [n["id"] for n in rest] == ["idea:yolgiz"]


def test_unselected_ideas_and_other_nodes_pass_through_unchanged():
    g = graph()
    out, _ = gi.build_grouped(g, [["idea:kibr", "idea:manmanlik"]], {"kibr": "Axloq"})
    by_id = {n["id"]: n for n in out["nodes"]}
    orig = {n["id"]: n for n in g["nodes"]}
    assert by_id["idea:yolgiz"] == orig["idea:yolgiz"] and "theme" not in by_id["idea:yolgiz"]
    assert by_id["person:ali"] == orig["person:ali"]


# --- parsing ---


LABELS = ["hasad", "kibr", "manmanlik", "Sabr"]


def test_parse_clusters_valid_unknown_and_bad_json():
    clusters, rejected = gi.parse_clusters('{"clusters": [["kibr", "manmanlik"]]}', LABELS)
    assert sorted(map(sorted, clusters)) == [["Sabr"], ["hasad"], ["kibr", "manmanlik"]] and rejected == 0
    clusters, rejected = gi.parse_clusters('{"clusters": [["kibr", "ego"]]}', LABELS)
    assert rejected == 1 and all(len(c) == 1 for c in clusters)
    with pytest.raises(gi.BadJsonError):
        gi.parse_clusters("not json", LABELS)


def test_parse_themes_valid():
    text = json.dumps({"themes": [{"name": "Axloq", "ideas": ["hasad", "kibr"]},
                                  {"name": "Iroda", "ideas": ["manmanlik", "Sabr"]}]})
    themes, stats = gi.parse_themes(text, LABELS)
    assert themes == {"hasad": "Axloq", "kibr": "Axloq", "manmanlik": "Iroda", "Sabr": "Iroda"}
    assert stats == {"unknown": 0, "duplicate": 0, "missing": 0}


def test_parse_themes_duplicate_missing_and_unknown():
    text = json.dumps({"themes": [{"name": "Axloq", "ideas": ["hasad", "kibr", "ego"]},
                                  {"name": "Iroda", "ideas": ["kibr", "Sabr"]}]})
    themes, stats = gi.parse_themes(text, LABELS)
    assert themes["kibr"] == "Axloq"  # first one wins
    assert themes["manmanlik"] == gi.OTHER_THEME  # missing goes to boshqa
    assert stats == {"unknown": 1, "duplicate": 1, "missing": 1}
    with pytest.raises(gi.BadJsonError):
        gi.parse_themes('{"themes": 3}', LABELS)


# --- label ---


def test_label_is_member_in_most_essays_tie_goes_to_longer():
    g = graph()
    out, _ = gi.build_grouped(g, [["idea:hasad", "idea:kibr"]], {"hasad": "Axloq"})
    node = next(n for n in out["nodes"] if n["id"] == "idea:hasad")
    assert node["label"] == "hasad" and set(node["aliases"]) == {"kibr", "Kibr"}
    out, _ = gi.build_grouped(g, [["idea:kibr", "idea:manmanlik"]], {"manmanlik": "Axloq"})
    node = next(n for n in out["nodes"] if n["label"] == "manmanlik")
    assert node["id"] == "idea:manmanlik"
    assert node["essays"] == ["001_a", "002_b", "004_d"] and node["mention_count"] == 5
    assert set(node["descriptions"]) == {"001_a", "002_b", "004_d"}


# --- overrides ---


def nodes_by_label():
    selected, _ = gi.select_ideas(graph())
    return {n["label"]: n for n in selected}


def test_overrides_merge_keep_apart_label_theme():
    groups = [["idea:hasad"], ["idea:kibr", "idea:manmanlik", "idea:sabr"]]
    ov = {"merge": [["hasad", "Kibr"]], "keep_apart": [["kibr", "Sabr"]], "label": {"kibr": "Takabburlik"}}
    groups, labels, warnings = gi.apply_merge_overrides(groups, nodes_by_label(), ov)
    find = lambda i: next(g for g in groups if i in g)
    assert "idea:kibr" in find("idea:hasad") or "idea:sabr" in find("idea:hasad")  # merge applied
    assert find("idea:kibr") is not find("idea:sabr")  # keep_apart applied
    assert sum(map(len, groups)) == 4 and warnings == []
    assert list(labels.values()) == ["Takabburlik"]

    themes, warnings = gi.apply_theme_overrides({"hasad": "Axloq", "Sabr": "Iroda"},
                                                {"theme": {"sabr": "Axloq"}}, {"Sabr": ["Sabr"]})
    assert themes == {"hasad": "Axloq", "Sabr": "Axloq"} and warnings == []


def test_overrides_unknown_names_warn_and_do_not_crash():
    groups = [["idea:hasad"], ["idea:kibr"]]
    ov = {"merge": [["hasad", "nomalum"]], "keep_apart": [["yoq"]], "label": {"bor emas": "x"}}
    groups, labels, warnings = gi.apply_merge_overrides(groups, nodes_by_label(), ov)
    assert groups == [["idea:hasad"], ["idea:kibr"]] and labels == {}
    assert len(warnings) == 3
    themes, warnings = gi.apply_theme_overrides({"hasad": "Axloq"}, {"theme": {"ego": "Axloq"}}, {"hasad": ["hasad"]})
    assert themes == {"hasad": "Axloq"} and len(warnings) == 1


# --- graph build ---


def test_graph_links_balance_no_dangling_one_in_theme_per_merged_idea():
    g = graph()
    groups = [["idea:hasad"], ["idea:kibr", "idea:manmanlik"], ["idea:sabr"]]
    themes = {"hasad": "Axloq", "manmanlik": "Axloq", "Sabr": "Iroda"}
    out, stats = gi.build_grouped(g, groups, themes)
    relation = [l for l in out["links"] if l["kind"] != "in_theme"]
    assert stats["self_loops"] == 1 and stats["folded_mentions"] == 1
    assert len(relation) == len(g["links"]) - stats["self_loops"] - stats["folded_mentions"]
    ids = {n["id"] for n in out["nodes"]}
    assert all(l["source"] in ids and l["target"] in ids for l in out["links"])
    in_theme = [l for l in out["links"] if l["kind"] == "in_theme"]
    merged = [n for n in out["nodes"] if "theme" in n]
    assert len(merged) == 3 and sorted(l["source"] for l in in_theme) == sorted(n["id"] for n in merged)
    assert {n["id"] for n in out["nodes"] if n["type"] == "theme"} == {"theme:axloq", "theme:iroda"}
    folded = next(l for l in out["links"] if l["kind"] == "mentioned_in" and l["target"] == "essay:002_b")
    assert folded["paragraphs"] == ["p2", "p3", "p10"]
    crit = next(l for l in out["links"] if l["kind"] == "criticises")
    assert crit["target"] == "idea:manmanlik"


def test_label_override_keeps_node_id():
    out, _ = gi.build_grouped(graph(), [["idea:kibr", "idea:manmanlik"]], {"Takabburlik": "Axloq"},
                              labels={"idea:kibr": "Takabburlik"})
    node = next(n for n in out["nodes"] if n.get("theme"))
    assert node["id"] == "idea:manmanlik" and node["label"] == "Takabburlik" and "manmanlik" in node["aliases"]


# --- cli call, cache, offline (fake subprocess) ---


@pytest.fixture
def fake_cli(monkeypatch):
    calls = []
    stdout = (FIXTURES / "fake_group_cli_stdout.json").read_text(encoding="utf-8")

    def run(args, **kw):
        calls.append(kw)
        return subprocess.CompletedProcess(args, 0, stdout=stdout, stderr="")

    monkeypatch.setattr(extract.subprocess, "run", run)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-or-v1-should-not-leak")
    return calls


def test_cached_call_runs_cli_once_then_uses_cache(tmp_path, fake_cli):
    text, status = gi.cached_call("merge", "sys", "prompt", tmp_path, force=False, offline=False)
    assert status == "ok" and json.loads(text)["clusters"] == [["kibr", "manmanlik"]]
    assert "ANTHROPIC_API_KEY" not in fake_cli[0]["env"]
    gi.cached_call("merge", "sys", "prompt", tmp_path, force=False, offline=False)
    assert len(fake_cli) == 1 and len(list((tmp_path / "raw").glob("merge_*.json"))) == 1


def test_offline_without_cache_returns_no_raw(tmp_path, fake_cli):
    text, status = gi.cached_call("themes", "sys", "prompt", tmp_path, force=False, offline=True)
    assert text is None and status == "no_raw" and fake_cli == []
