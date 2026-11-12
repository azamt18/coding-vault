"""Tests for retrieve.py: offline, no model calls."""

import json

import retrieve

PARS = [
    {"id": "001_a#p1", "essay": "001_a", "title": "Qora oqqush", "source": "https://parallelmuhit.uz/a",
     "text": "Taleb antifragil tizimlar haqida yozadi. Tizim stressdan kuchayadi.", "links": []},
    {"id": "001_a#p2", "essay": "001_a", "title": "Qora oqqush", "source": "https://parallelmuhit.uz/a",
     "text": "Bugun havo issiq edi, daraxtlar soya berdi.", "links": []},
    {"id": "002_b#p1", "essay": "002_b", "title": "Kitoblar", "source": "https://parallelmuhit.uz/b",
     "text": "Men Atomic Habits kitobini hammaga tavsiya qilaman.", "links": []},
]
NODES = [
    {"id": "author:aziz-rahimov", "label": "Aziz Rahimov", "type": "author"},
    {"id": "essay:001_a", "label": "Qora oqqush", "type": "essay"},
    {"id": "person:taleb", "label": "Nassim Taleb", "type": "person", "aliases": ["Taleb", "Talebning"]},
    {"id": "work:ah", "label": "Atomic Habits", "type": "work", "aliases": []},
    {"id": "person:ali", "label": "Ali", "type": "person", "aliases": []},
]
LINKS = [
    {"source": "author:aziz-rahimov", "target": "essay:001_a", "kind": "wrote", "essay": "001_a"},
    {"source": "author:aziz-rahimov", "target": "work:ah", "kind": "recommends", "essay": "002_b",
     "paragraph": "p1", "quote": "Men Atomic Habits kitobini hammaga tavsiya qilaman."},
    {"source": "author:aziz-rahimov", "target": "person:taleb", "kind": "inspired_by", "essay": "001_a",
     "paragraph": "p1", "quote": "Taleb antifragil tizimlar haqida yozadi."},
]


def test_fold_drops_apostrophes_and_case():
    assert retrieve.fold("O‘rmon  BO'LDI") == "ormon boldi"


def test_tokens_stem_to_five_letters_and_drop_stopwords():
    assert retrieve.tokens("Taleb haqida nima deydi") == ["taleb", "deydi"]
    assert retrieve.tokens("antifragillik") == ["antif"]


def test_bm25_ranks_the_relevant_paragraph_first():
    bm = retrieve.BM25(PARS)
    ranked = bm.search("antifragil tizimlar", 3)
    assert ranked[0][0] == "001_a#p1"
    assert "001_a#p2" not in [i for i, _ in ranked]  # zero-score paragraphs are not returned


def test_find_entities_matches_suffixed_forms_and_skips_essay_author():
    ids = retrieve.find_entities("Aziz Rahimov Talebning fikri qanday?", NODES)
    assert ids == ["person:taleb"]


def test_find_entities_needs_min_length():
    assert retrieve.find_entities("aliqanday gap", NODES) == []


def test_retrieve_merges_graph_and_text_and_caps():
    corpus = {p["id"]: p for p in PARS}
    ctx = retrieve.retrieve("Taleb haqida nima deydi?", corpus, retrieve.BM25(PARS), NODES, LINKS,
                            max_paragraphs=2, max_links=1)
    assert [l["paragraph_id"] for l in ctx["links"]] == ["001_a#p1"]
    assert "001_a#p1" in [p["id"] for p in ctx["paragraphs"]]
    assert len(ctx["paragraphs"]) <= 2
    assert retrieve.allowed_ids(ctx) >= {"001_a#p1"}


def test_graph_hits_come_first_when_text_does_not_match():
    corpus = {p["id"]: p for p in PARS}
    ctx = retrieve.retrieve("Atomic Habits", corpus, retrieve.BM25(PARS), NODES, LINKS)
    assert ctx["paragraphs"][0]["id"] == "002_b#p1"
    assert ctx["links"][0]["kind"] == "recommends"


def test_load_corpus_reads_sonnet_json(tmp_path):
    d = {"essay": {"id": "001_a", "title": "T", "source": "https://x/a"},
         "paragraphs": [{"id": "p1", "global_id": "001_a#p1", "text": "salom", "links": [{"text": "s", "url": "https://u"}]}]}
    (tmp_path / "001_a.json").write_text(json.dumps(d))
    (tmp_path / "001_a.review.md").write_text("x")
    c = retrieve.load_corpus(tmp_path)
    assert c["001_a#p1"]["source"] == "https://x/a"
    assert c["001_a#p1"]["links"][0]["url"] == "https://u"
