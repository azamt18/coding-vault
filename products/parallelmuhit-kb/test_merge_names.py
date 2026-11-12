"""Tests for merge_names.py. No model calls: the cli is a fake subprocess."""

import json
import subprocess
from pathlib import Path

import pytest

import extract
import merge_names as mn

FIXTURES = Path(__file__).parent / "fixtures"
AUTHOR = extract.AUTHOR


def ent(name, etype="person", base=None, desc="tavsif", paragraphs=("p1",)):
    return {"name": name, "base_name": base or name, "type": etype, "description": desc, "aliases": [],
            "paragraphs": list(paragraphs)}


def rel(source, target, kind="inspired_by", quote="iqtibos", paragraph="p1"):
    return {"source": source, "target": target, "kind": kind, "label": "l", "paragraph": paragraph, "quote": quote}


def result(eid, entities, relations=()):
    number = int(eid[:3])
    return {"essay": {"id": eid, "number": number, "slug": eid[4:], "title": f"T {eid}",
                      "source": f"https://parallelmuhit.uz/{eid[4:]}"},
            "author": {"name": AUTHOR}, "entities": list(entities), "relations": list(relations)}


# --- normalization and blocking ---


def test_normalize_folds_apostrophes_doubles_and_spellings():
    assert mn.normalize("Charli Munger") == mn.normalize("charli munger")
    assert mn.normalize("Uorren Buffett") == mn.normalize("Uorren Bufet")
    assert mn.normalize("Nassim Taleb") == mn.normalize("Nasim Taleb")
    assert mn.normalize("Yo‘lchi") == mn.normalize("Yolchi") == mn.normalize("Yo'lchi")
    assert mn.normalize("Yevropa") == mn.normalize("Evropa")
    assert mn.normalize("Maksim") == mn.normalize("Maxim")
    assert "sh" in mn.normalize("Shoir") and "ch" in mn.normalize("Chamat")


def test_munger_variants_share_a_block_unrelated_names_dont():
    names = ["Charli Munger", "Charlie Manger", "Munger", "Manger", "Ilon Mask", "Suqrot", "Nassim Taleb", "Taleb"]
    blocks = mn.build_blocks(names)
    find = lambda n: next(b for b in blocks if n in b)
    assert set(find("Munger")) >= {"Charli Munger", "Charlie Manger", "Munger", "Manger"}
    assert "Ilon Mask" not in find("Munger") and "Suqrot" not in find("Munger")
    assert set(find("Taleb")) == {"Nassim Taleb", "Taleb"}
    assert find("Suqrot") == ["Suqrot"]


def test_big_blocks_are_split_and_capped():
    names = [f"Ali {x}{y}ov" for x in "abcdefgh" for y in "abcdefgh"]  # 64 names sharing nothing but a pattern
    names += [f"{x} Karimov" for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] * 1 + [f"{x}a Karimov" for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    for b in mn.build_blocks(names):
        assert len(b) <= mn.MAX_BLOCK


# --- compound split ---


def test_compound_split_when_all_parts_known():
    results = [
        result("001_a", [ent("Buffet"), ent("Munger")]),
        result("002_b", [ent("Buffet va Munger"), ent("qiziqish", "idea")],
               [rel("Buffet va Munger", "qiziqish"), rel(AUTHOR, "Buffet va Munger", "recommends")]),
    ]
    out, stats = mn.split_compounds(results)
    names = sorted(e["base_name"] for e in out[1]["entities"])
    assert names == ["Buffet", "Munger", "qiziqish"]
    assert stats == {"splits": 1, "copied_links": 2}
    pairs = sorted((r["source"], r["target"]) for r in out[1]["relations"])
    assert pairs == [(AUTHOR, "Buffet"), (AUTHOR, "Munger"), ("Buffet", "qiziqish"), ("Munger", "qiziqish")]
    assert results[1]["entities"][0]["name"] == "Buffet va Munger"  # input untouched


def test_compound_left_alone_when_a_part_is_unknown():
    results = [result("001_a", [ent("Rik", "person")]),
               result("002_b", [ent("Rik va Morti", "work")], [rel(AUTHOR, "Rik va Morti", "recommends")])]
    out, stats = mn.split_compounds(results)
    assert [e["name"] for e in out[1]["entities"]] == ["Rik va Morti"]
    assert stats == {"splits": 0, "copied_links": 0}


# --- cluster parsing ---


def test_parse_valid_clusters_fills_singletons():
    block = ["Charli Munger", "Charlie Manger", "Munger", "Charli Mungerson"]
    clusters, rejected = mn.parse_clusters('{"clusters": [["Charli Munger", "Munger"]]}', block)
    assert rejected == 0
    assert sorted(map(sorted, clusters)) == [["Charli Munger", "Munger"], ["Charli Mungerson"], ["Charlie Manger"]]


def test_parse_rejects_cluster_with_a_name_outside_the_block():
    block = ["Charli Munger", "Munger"]
    clusters, rejected = mn.parse_clusters('{"clusters": [["Charli Munger", "Uorren Baffet"], ["Munger"]]}', block)
    assert rejected == 1
    assert sorted(map(sorted, clusters)) == [["Charli Munger"], ["Munger"]]


def test_parse_rejects_a_name_used_twice():
    block = ["A", "B", "C"]
    clusters, rejected = mn.parse_clusters('{"clusters": [["A", "B"], ["B", "C"]]}', block)
    assert rejected == 1 and sorted(map(sorted, clusters)) == [["A", "B"], ["C"]]


@pytest.mark.parametrize("text", ["not json", '```json\n{"clusters": []}\n```', '{"groups": []}', '{"clusters": "x"}'])
def test_parse_bad_json_raises(text):
    with pytest.raises(extract.BadJson):
        mn.parse_clusters(text, ["A", "B"])


# --- label ---


def test_label_is_spelling_in_most_essays_tie_goes_to_longer():
    spellings = {"Munger": {"001_a", "002_b"}, "Charli Munger": {"003_c", "004_d", "005_e"}, "Manger": {"006_f"}}
    label, aliases = mn.choose_label(spellings, extra_names={"Charli Mungerning"})
    assert label == "Charli Munger"
    assert aliases == ["Charli Mungerning", "Manger", "Munger"]
    label, _ = mn.choose_label({"Taleb": {"001_a"}, "Nassim Taleb": {"002_b"}})
    assert label == "Nassim Taleb"


# --- overrides ---


def _clusters():
    return [mn.Cluster("person", ["Charli Munger", "Munger"]), mn.Cluster("person", ["Manger"]),
            mn.Cluster("person", ["Ernst Baffet", "Uorren Baffet"]), mn.Cluster("work", ["Antifragil"])]


def test_override_merge_and_keep_apart_and_label():
    overrides = {"merge": [["Munger", "Manger"]], "keep_apart": [["Uorren Baffet", "Ernst Baffet"]],
                 "label": {"Munger": "Charlie Munger"}}
    clusters, warnings = mn.apply_overrides(_clusters(), overrides)
    members = sorted(sorted(c.members) for c in clusters)
    assert ["Charli Munger", "Manger", "Munger"] in members
    assert ["Ernst Baffet"] in members and ["Uorren Baffet"] in members
    munger = next(c for c in clusters if "Munger" in c.members)
    assert munger.label_override == "Charlie Munger"
    assert warnings == []


def test_override_with_unknown_name_warns_and_does_not_crash():
    overrides = {"merge": [["Munger", "Nobody"]], "keep_apart": [["Ghost", "Munger"]], "label": {"Phantom": "X"}}
    clusters, warnings = mn.apply_overrides(_clusters(), overrides)
    assert len(warnings) == 3 and all("unknown" in w for w in warnings)
    assert sorted(sorted(c.members) for c in clusters) == sorted(sorted(c.members) for c in _clusters())


def test_override_merge_across_types_warns():
    clusters, warnings = mn.apply_overrides(_clusters(), {"merge": [["Munger", "Antifragil"]]})
    assert len(warnings) == 1 and "type" in warnings[0]


# --- graph ---


def _corpus():
    return [
        result("001_a", [ent("Charli Mungerning", base="Charli Munger"), ent("kibr", "idea", "Kibr")],
               [rel("Charli Mungerning", "kibr", "counterexample_of"), rel(AUTHOR, "Charli Mungerning")]),
        result("002_b", [ent("Munger"), ent("Charli Munger"), ent("Kibr", "idea")],
               [rel("Munger", "Kibr", "counterexample_of"), rel("Munger", "Charli Munger", "associated_with")]),
        result("003_c", [ent("Buffet va Munger"), ent("Buffet")], [rel("Buffet va Munger", "Buffet", "associated_with")]),
    ]


def test_graph_links_balance_and_endpoints_exist():
    results = _corpus()
    split, stats = mn.split_compounds(results)
    clusters = [mn.Cluster("person", ["Charli Munger", "Munger"]), mn.Cluster("person", ["Buffet"])]
    graph, gstats = mn.build_graph(split, clusters)
    input_links = sum(len(r["relations"]) for r in results)
    quoted = [l for l in graph["links"] if l["kind"] not in ("mentioned_in",) and "quote" in l]
    assert len(quoted) == input_links + stats["copied_links"] - gstats["self_loops"]
    assert gstats["self_loops"] == 2  # Munger—Charli Munger in 002, Buffet—Buffet after the split in 003
    ids = {n["id"] for n in graph["nodes"]}
    assert all(l["source"] in ids and l["target"] in ids for l in graph["links"])


def test_graph_nodes_ideas_merge_on_exact_base_name_and_labels():
    graph, _ = mn.build_graph(mn.split_compounds(_corpus())[0],
                              [mn.Cluster("person", ["Charli Munger", "Munger"]), mn.Cluster("person", ["Buffet"])])
    by_label = {n["label"]: n for n in graph["nodes"]}
    munger = by_label["Charli Munger"]
    assert munger["type"] == "person" and munger["essays"] == ["001_a", "002_b", "003_c"]
    assert "Munger" in munger["aliases"] and "Charli Mungerning" in munger["aliases"]
    assert set(munger["descriptions"]) == {"001_a", "002_b", "003_c"}
    kibr = [n for n in graph["nodes"] if n["type"] == "idea"]
    assert len(kibr) == 1 and kibr[0]["essays"] == ["001_a", "002_b"]
    assert any(n["type"] == "essay" for n in graph["nodes"]) and any(n["type"] == "author" for n in graph["nodes"])
    kinds = {l["kind"] for l in graph["links"]}
    assert "mentioned_in" in kinds and "wrote" in kinds
    wrote_essays = [l for l in graph["links"] if l["kind"] == "wrote" and l["target"].startswith("essay:")]
    assert len(wrote_essays) == 3


def test_node_ids_are_stable_slugs_and_unique():
    clusters = [mn.Cluster("person", ["Taleb"]), mn.Cluster("person", ["taleb kitobi"])]
    graph, _ = mn.build_graph([result("001_a", [ent("Taleb"), ent("O‘tkir Hoshimov")])], clusters)
    ids = [n["id"] for n in graph["nodes"]]
    assert len(ids) == len(set(ids))
    assert "person:taleb" in ids and "person:otkir-hoshimov" in ids


# --- cli call, cache, offline (fake subprocess) ---


@pytest.fixture
def fake_cli(monkeypatch):
    calls = []
    stdout = (FIXTURES / "fake_merge_cli_stdout.json").read_text(encoding="utf-8")

    def run(args, input=None, capture_output=None, text=None, env=None, cwd=None, timeout=None):
        calls.append({"args": args, "input": input, "env": env})
        return subprocess.CompletedProcess(args, 0, stdout=stdout, stderr="")

    monkeypatch.setattr(extract.subprocess, "run", run)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-or-v1-should-not-leak")
    return calls


def test_cluster_block_calls_cli_once_then_uses_cache(tmp_path, fake_cli):
    block = mn.Block("person", ["Charli Munger", "Charli Mungerson", "Charlie Manger", "Munger"])
    info = {n: {"description": "investor", "essays": 2, "quote": "q"} for n in block.names}
    out = tmp_path / "merge"
    clusters, status = mn.cluster_block(block, info, out, force=False, offline=False)
    assert status == "ok" and len(fake_cli) == 1
    call = fake_cli[0]
    assert "ANTHROPIC_API_KEY" not in call["env"]
    assert call["args"][call["args"].index("--model") + 1] == "claude-sonnet-5-5"
    assert call["args"][call["args"].index("--system-prompt") + 1] == mn.SYSTEM
    assert "Charlie Manger" in call["input"] and "investor" in call["input"]
    assert sorted(map(sorted, clusters)) == [["Charli Munger", "Charlie Manger", "Munger"], ["Charli Mungerson"]]
    again, status = mn.cluster_block(block, info, out, force=False, offline=True)
    assert again == clusters and status == "ok" and len(fake_cli) == 1


def test_offline_without_cache_keeps_names_apart(tmp_path, fake_cli):
    block = mn.Block("person", ["A", "B"])
    clusters, status = mn.cluster_block(block, {n: {"description": "", "essays": 1, "quote": ""} for n in "AB"},
                                        tmp_path, force=False, offline=True)
    assert status == "no_raw" and sorted(clusters) == [["A"], ["B"]] and fake_cli == []


def test_block_ids_are_stable():
    a = mn.Block("person", ["Munger", "Charli Munger"])
    b = mn.Block("person", ["Charli Munger", "Munger"])
    assert a.id == b.id and a.id.startswith("person_")
