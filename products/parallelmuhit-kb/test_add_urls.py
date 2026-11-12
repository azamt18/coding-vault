"""Tests for add_urls.py: offline, no model calls."""

import json
from pathlib import Path

import pytest

import add_urls

MD = """\
---
number: 3
slug: javoblar
title: "Javoblar"
author: Aziz Rahimov
source: https://parallelmuhit.uz/javoblar
---

Birinchi paragraf.

Shahboz Dolimov bilan suhbatga [qarang](https://youtu.be/abc). Kitob: [Atomic Habits](https://example.com/ah).
"""


def sonnet_result(links=None):
    return {"essay": {"id": "003_javoblar"},
            "paragraphs": [{"id": "p1", "global_id": "003_javoblar#p1", "text": "Birinchi paragraf."},
                           {"id": "p2", "global_id": "003_javoblar#p2",
                            "text": "Shahboz Dolimov bilan suhbatga qarang. Kitob: Atomic Habits."}]}


def graph():
    return {
        "nodes": [
            {"id": "author:aziz-rahimov", "label": "Aziz Rahimov", "type": "author"},
            {"id": "essay:003_javoblar", "label": "Javoblar", "type": "essay"},
            {"id": "person:shahboz-dolimov", "label": "Shahboz Dolimov", "type": "person", "aliases": []},
            {"id": "work:atomic-habits", "label": "Atomic habits", "type": "work", "aliases": ["Atomic Habits"]},
        ],
        "links": [
            {"source": "author:aziz-rahimov", "target": "person:shahboz-dolimov", "kind": "recommends",
             "essay": "003_javoblar", "paragraph": "p2", "quote": "Shahboz Dolimov bilan suhbatga qarang."},
            {"source": "author:aziz-rahimov", "target": "work:atomic-habits", "kind": "recommends",
             "essay": "003_javoblar", "paragraph": "p2", "quote": "Kitob: Atomic Habits."},
            {"source": "work:atomic-habits", "target": "essay:003_javoblar", "kind": "mentioned_in",
             "essay": "003_javoblar", "paragraphs": ["p1", "p2"]},
        ],
    }


def test_patch_paragraphs_adds_links_by_global_id():
    r = sonnet_result()
    n = add_urls.patch_paragraphs(r, MD)
    assert r["paragraphs"][0]["links"] == []
    assert [l["url"] for l in r["paragraphs"][1]["links"]] == ["https://youtu.be/abc", "https://example.com/ah"]
    assert n == 2


def test_patch_paragraphs_fails_loudly_when_text_changed():
    r = sonnet_result()
    r["paragraphs"][1]["text"] = "boshqa matn"
    with pytest.raises(ValueError, match="003_javoblar#p2"):
        add_urls.patch_paragraphs(r, MD)


def test_attach_urls_to_links_and_nodes_end_to_end():
    r = sonnet_result()
    add_urls.patch_paragraphs(r, MD)
    g, stats = add_urls.attach_urls(graph(), [r])
    l = g["links"]
    # the anchor "qarang" lies inside the first quote, so the link gets the youtube url
    assert l[0]["urls"] == [{"text": "qarang", "url": "https://youtu.be/abc"}]
    assert l[1]["urls"] == [{"text": "Atomic Habits", "url": "https://example.com/ah"}]
    # mentioned_in gets every url of its paragraphs
    assert [u["url"] for u in l[2]["urls"]] == ["https://youtu.be/abc", "https://example.com/ah"]
    nodes = {n["id"]: n for n in g["nodes"]}
    assert nodes["work:atomic-habits"]["urls"] == [{"text": "Atomic Habits", "url": "https://example.com/ah"}]
    assert "urls" not in nodes["person:shahboz-dolimov"]  # "qarang" is no name
    assert "urls" not in nodes["essay:003_javoblar"]
    assert stats["urls_total"] == 2 and stats["urls_attached"] == 2 and stats["urls_left_out"] == 0


def test_left_out_urls_are_counted():
    r = sonnet_result()
    add_urls.patch_paragraphs(r, MD)
    g = graph()
    g["links"] = g["links"][:1]  # only the "qarang" link survives
    g["nodes"] = [n for n in g["nodes"] if n["id"] != "work:atomic-habits"]
    _, stats = add_urls.attach_urls(g, [r])
    assert stats["urls_attached"] == 1 and stats["urls_left_out"] == 1


def test_rerun_is_byte_identical_and_idempotent():
    r = sonnet_result()
    add_urls.patch_paragraphs(r, MD)
    g1, _ = add_urls.attach_urls(graph(), [r])
    g2, _ = add_urls.attach_urls(json.loads(json.dumps(g1)), [r])
    assert json.dumps(g1, sort_keys=True) == json.dumps(g2, sort_keys=True)
    add_urls.patch_paragraphs(r, MD)
    assert r == json.loads(json.dumps(r))
