"""Retrieval for the q&a (task 08): bm25 over paragraphs + 1-hop graph links, merged and capped.

No embeddings, no model calls. Uzbek is agglutinative, so every token is cut to its first 5 letters.
"""

import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

APOSTROPHES = re.compile(r"[‘ʻ'’`ʼ]")  # same set as ui/src/search.ts and merge_names.py
STOP = {
    "va", "bu", "shu", "bilan", "uchun", "ham", "esa", "nima", "qanday", "haqida", "qaysi", "kim", "qachon",
    "lekin", "agar", "bir", "men", "siz", "biz", "ular", "yani", "deb", "dan", "ning", "ga", "ni", "da", "mi",
    "nega", "qaerda", "qancha", "bor", "yoq", "edi", "ekan", "aytadi", "fikri",
}
STEM = 5
EXCLUDED_TYPES = {"essay", "author", "theme"}  # every question names the author; essays/themes are not entities
MIN_NAME = 4


def fold(s: str) -> str:
    return re.sub(r"\s+", " ", APOSTROPHES.sub("", unicodedata.normalize("NFC", s).lower())).strip()


def tokens(text: str) -> list[str]:
    words = re.findall(r"[^\W_]+", fold(text))
    return [w[:STEM] for w in words if len(w) >= 3 and w not in STOP]


class BM25:
    def __init__(self, paragraphs: list[dict], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.ids = [p["id"] for p in paragraphs]
        self.tf = [Counter(tokens(p["text"])) for p in paragraphs]
        self.len = [sum(t.values()) for t in self.tf]
        self.avg = (sum(self.len) / len(self.len)) if self.len else 0.0
        df = Counter(w for t in self.tf for w in t)
        n = len(self.tf)
        self.idf = {w: math.log(1 + (n - d + 0.5) / (d + 0.5)) for w, d in df.items()}

    def score(self, query_tokens: list[str], i: int) -> float:
        s = 0.0
        for w in set(query_tokens):
            f = self.tf[i].get(w, 0)
            if f:
                s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[i] / (self.avg or 1)))
        return s

    def search(self, query: str, k: int) -> list[tuple[str, float]]:
        q = tokens(query)
        scored = [(self.ids[i], self.score(q, i)) for i in range(len(self.ids))]
        scored = [x for x in scored if x[1] > 0]
        scored.sort(key=lambda x: -x[1])
        return scored[:k]


def load_corpus(sonnet_dir: Path) -> dict[str, dict]:
    """global paragraph id -> {id, essay, title, source, text, links}, from extract/sonnet/*.json."""
    corpus: dict[str, dict] = {}
    for f in sorted(Path(sonnet_dir).glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        e = d["essay"]
        for p in d["paragraphs"]:
            corpus[p["global_id"]] = {"id": p["global_id"], "essay": e["id"], "title": e.get("title", ""),
                                      "source": e.get("source", ""), "text": p["text"], "links": p.get("links", [])}
    return corpus


def find_entities(question: str, nodes: list[dict]) -> list[str]:
    """ids of nodes whose label/alias starts a word in the question (so suffixed forms match)."""
    q = fold(question)
    found = []
    for n in nodes:
        if n["type"] in EXCLUDED_TYPES:
            continue
        for name in [n["label"], *n.get("aliases", [])]:
            name = fold(name)
            if len(name) >= MIN_NAME and re.search(r"(?<!\w)" + re.escape(name), q):
                found.append(n["id"])
                break
    return found


def retrieve(question: str, corpus: dict, bm25: BM25, nodes: list[dict], links: list[dict],
             max_paragraphs: int = 12, max_links: int = 20) -> dict:
    label = {n["id"]: n["label"] for n in nodes}
    ents = set(find_entities(question, nodes))
    qt = tokens(question)

    cand = []
    for l in links:
        if l["kind"] == "wrote" or not l.get("quote") or not l.get("paragraph"):
            continue
        if l["source"] in ents or l["target"] in ents:
            pid = f"{l['essay']}#{l['paragraph']}"
            if pid in corpus:
                cand.append((len(set(qt) & set(tokens(l["quote"]))), l, pid))
    cand.sort(key=lambda x: -x[0])  # stable: ties keep graph order
    chosen = [{"kind": l["kind"], "label": l.get("label", ""), "quote": l["quote"], "paragraph_id": pid,
               "essay": l["essay"], "source": label.get(l["source"], l["source"]),
               "target": label.get(l["target"], l["target"]), "urls": l.get("urls", [])}
              for _, l, pid in cand[:max_links]]

    text_hits = dict(bm25.search(question, 50))
    bonus = (max(text_hits.values()) if text_hits else 0) + 1  # graph-linked paragraphs outrank pure text hits
    score = dict(text_hits)
    for l in chosen:
        score[l["paragraph_id"]] = score.get(l["paragraph_id"], 0) + bonus
    top = sorted(score, key=lambda i: -score[i])[:max_paragraphs]
    return {"entities": sorted(ents), "paragraphs": [corpus[i] for i in top], "links": chosen}


def allowed_ids(ctx: dict) -> set[str]:
    return {p["id"] for p in ctx["paragraphs"]} | {l["paragraph_id"] for l in ctx["links"]}
