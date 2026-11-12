"""Tests for ask.py: offline, the model is an injected function."""

import ask
import retrieve
from test_retrieve import LINKS, NODES, PARS


def run(answer, question="Taleb haqida nima deydi?"):
    corpus = {p["id"]: p for p in PARS}
    return ask.ask(question, corpus, retrieve.BM25(PARS), NODES, LINKS, generate=lambda system, prompt: answer)


def test_valid_citation_kept_and_quote_copied_by_code():
    r = run("Taleb antifragillikni yozadi [001_a#p1].")
    assert r["flagged"] is False
    assert r["citations"][0]["id"] == "001_a#p1"
    assert r["citations"][0]["quote"] == "Taleb antifragil tizimlar haqida yozadi."  # link quote, exact
    assert r["citations"][0]["url"] == "https://parallelmuhit.uz/a"


def test_fake_citation_dropped_and_flagged():
    r = run("Bu gap [999_x#p1] va bu [001_a#p1].")
    assert "999_x#p1" not in r["answer"]
    assert r["dropped"] == ["999_x#p1"]
    assert r["flagged"] is True
    assert [c["id"] for c in r["citations"]] == ["001_a#p1"]


def test_id_that_exists_but_is_not_in_the_context_is_fake():
    r = run("Gap [001_a#p2].")  # p2 is in the corpus but was not retrieved
    assert r["dropped"] == ["001_a#p2"] and r["flagged"] is True


def test_multi_id_bracket_is_split():
    r = run("Gap [001_a#p1, 999_x#p9].")
    assert r["dropped"] == ["999_x#p9"]
    assert [c["id"] for c in r["citations"]] == ["001_a#p1"]


def test_answer_without_any_valid_citation_is_flagged():
    assert run("Taleb haqida bilmayman, lekin yozgan.")["flagged"] is True


def test_not_found_answer_is_not_flagged():
    r = run("essalarda bu haqda topilmadi")
    assert r["flagged"] is False and r["citations"] == []


def test_citation_without_link_quote_uses_paragraph_text_and_urls():
    corpus = {p["id"]: dict(p) for p in PARS}
    corpus["002_b#p1"]["links"] = [{"text": "kitob", "url": "https://amazon/ah"}]
    r = ask.ask("Atomic Habits", corpus, retrieve.BM25(PARS), NODES, LINKS, generate=lambda s, p: "Tavsiya [002_b#p1].")
    c = r["citations"][0]
    assert c["quote"] in PARS[2]["text"]
    assert {"text": "kitob", "url": "https://amazon/ah"} in c["links"]


def test_prompt_lists_ids_and_rules():
    ctx = retrieve.retrieve("Taleb", {p["id"]: p for p in PARS}, retrieve.BM25(PARS), NODES, LINKS)
    prompt = ask.build_prompt("Taleb?", ctx)
    assert "[001_a#p1]" in prompt and "Taleb?" in prompt
    assert "essalarda bu haqda topilmadi" in ask.SYSTEM


def test_render_shows_answer_quotes_urls_and_flag():
    r = run("Gap [999_x#p1] [001_a#p1].")
    out = ask.render(r)
    assert "https://parallelmuhit.uz/a" in out and "001_a#p1" in out
    assert "999_x#p1" in out and "ogohlantirish" in out.lower()
