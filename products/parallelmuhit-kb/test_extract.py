"""Tests for extract.py. No network: the model is a fake client fed a recorded response."""

import json
from pathlib import Path

import pytest

import extract

FIXTURE = Path(__file__).parent / "fixtures" / "fake_extraction_response.json"

ESSAY_MD = """\
---
number: 149
slug: qiziquvchanlik
title: "Qiziquvchanlik: maktabdan keyin"
author: Aziz Rahimov
posted_by: Alijanov Ibrohim
created_at: '2026-05-28T18:53:32.062Z'
source: https://parallelmuhit.uz/qiziquvchanlik
---

# Qiziquvchanlik muallifni hayron qoldiradi

28.05.2026

O'rganishdan to'xtamaydigan odamlar. *Angliyada* yashaydigan vatandoshimiz [shuni](https://x.com/a) kuzatgan.

![](https://b.parallelmuhit.uz/api/images/x.jpg)

Shuning uchun Charli Manger **sohadan tashqari o'rganish ham muhimligini** ta'kidlaydi.

---

## Baffet haqida

> *Bir narsa aniqki, Uorren Baffet o‘rganmaganida, kompaniyamiz hozirgi holatining xiragina soyasi bo'lar edi.*
"""


@pytest.fixture
def essay():
    return extract.parse_essay(ESSAY_MD)


@pytest.fixture
def fake_raw():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class FakeClient:
    def __init__(self, raw):
        self.raw = raw
        self.calls = []
        self.messages = self

    def parse(self, **kwargs):
        self.calls.append(kwargs)
        raw = self.raw

        class Response:
            def model_dump(self, mode="python"):
                return raw

        return Response()


class NoNetworkClient:
    @property
    def messages(self):
        raise AssertionError("the api must not be called")


# --- paragraphs ---


def test_frontmatter_split_survives_body_rule(essay):
    assert essay["meta"]["number"] == 149
    assert essay["meta"]["title"] == "Qiziquvchanlik: maktabdan keyin"
    assert essay["id"] == "149_qiziquvchanlik"


def test_paragraphs_skip_date_image_and_rule_keep_headings(essay):
    assert [p["id"] for p in essay["paragraphs"]] == ["p1", "p2", "p3", "p4", "p5"]
    texts = [p["text"] for p in essay["paragraphs"]]
    assert texts[0] == "Qiziquvchanlik muallifni hayron qoldiradi"
    assert texts[3] == "Baffet haqida"


def test_markup_stripped_apostrophes_untouched(essay):
    texts = [p["text"] for p in essay["paragraphs"]]
    assert texts[1] == "O'rganishdan to'xtamaydigan odamlar. Angliyada yashaydigan vatandoshimiz shuni kuzatgan."
    assert texts[2] == "Shuning uchun Charli Manger sohadan tashqari o'rganish ham muhimligini ta'kidlaydi."
    assert texts[4] == (
        "Bir narsa aniqki, Uorren Baffet o‘rganmaganida, kompaniyamiz hozirgi holatining xiragina soyasi bo'lar edi."
    )


def test_plain_text_keeps_every_apostrophe_variant():
    s = "oʻzbek gʻoya ‘qoʻsh’ o'g'il"
    assert extract.plain_text(s) == s


def test_prompt_has_numbered_paragraphs_and_author(essay):
    prompt = extract.build_prompt(essay)
    assert "[p1] Qiziquvchanlik muallifni hayron qoldiradi" in prompt
    assert "[p5] Bir narsa aniqki" in prompt
    assert "Aziz Rahimov" in extract.SYSTEM and '"men"' in extract.SYSTEM and '"biz"' in extract.SYSTEM


# --- quote check ---


def test_quote_exact_match_passes(essay):
    assert extract.check_quote(essay, "p3", "sohadan tashqari o'rganish") is None


@pytest.mark.parametrize("variant", ["o‘", "oʻ", "o’", "o`"])
def test_quote_with_swapped_apostrophe_fails(essay, variant):
    assert extract.check_quote(essay, "p3", f"sohadan tashqari {variant}rganish") == "quote_not_found"


def test_quote_in_wrong_or_unknown_paragraph_fails(essay):
    assert extract.check_quote(essay, "p1", "sohadan tashqari o'rganish") == "quote_not_found"
    assert extract.check_quote(essay, "p42", "sohadan") == "bad_paragraph"
    assert extract.check_quote(essay, "p3", "") == "quote_not_found"


# --- validation of a recorded response ---


def test_validation_keeps_good_items_and_drops_with_reasons(essay, fake_raw):
    result = extract.build_result(essay, "haiku", fake_raw)

    assert [e["name"] for e in result["entities"]] == ["Charli Manger", "Qiziquvchanlik", "Berkshir"]
    assert [(r["source"], r["target"]) for r in result["relations"]] == [
        ("Charli Manger", "Qiziquvchanlik"),
        ("Aziz Rahimov", "Qiziquvchanlik"),
        ("Charli Manger", "Berkshir"),
        ("Berkshir", "Qiziquvchanlik"),
    ]
    assert result["relations"][-1]["kind"] == "counterexample_of"
    reasons = sorted(d["reason"] for d in result["dropped"])
    assert reasons == sorted(
        ["bad_type", "bad_paragraph", "quote_not_found", "quote_not_found", "bad_paragraph",
         "unknown_entity", "unknown_entity", "bad_kind"]
    )
    berkshir = next(e for e in result["entities"] if e["name"] == "Berkshir")
    assert berkshir["paragraphs"] == ["p5"]


def test_graph_pieces_built_by_code(essay, fake_raw):
    result = extract.build_result(essay, "haiku", fake_raw)
    assert result["essay"] == {
        "id": "149_qiziquvchanlik",
        "number": 149,
        "slug": "qiziquvchanlik",
        "title": "Qiziquvchanlik: maktabdan keyin",
        "source": "https://parallelmuhit.uz/qiziquvchanlik",
    }
    assert result["author"] == {"name": "Aziz Rahimov"}
    assert result["mentioned_in"][0] == {
        "entity": "Charli Manger",
        "essay": "149_qiziquvchanlik",
        "paragraphs": ["149_qiziquvchanlik#p3", "149_qiziquvchanlik#p5"],
    }
    assert len(result["mentioned_in"]) == 3
    assert result["paragraphs"][0] == {
        "id": "p1", "global_id": "149_qiziquvchanlik#p1", "text": "Qiziquvchanlik muallifni hayron qoldiradi",
        "links": [],
    }


def test_usage_and_cost(essay, fake_raw):
    result = extract.build_result(essay, "haiku", fake_raw)
    assert result["model"] == "claude-haiku-5-5"
    assert result["usage"] == {"input_tokens": 3000, "output_tokens": 1500}
    # haiku 5.5: $0.10 in / $0.50 out per 1M tokens
    assert result["cost_usd"] == pytest.approx(3000 * 0.10 / 1e6 + 1500 * 0.50 / 1e6)


def test_review_md(essay, fake_raw):
    md = extract.render_review(extract.build_result(essay, "haiku", fake_raw))
    assert "## person" in md and "## idea" in md and "## organization" in md
    assert "Charli Manger —recommends (muhimligini ta'kidlaydi)→ Qiziquvchanlik" in md
    assert "> sohadan tashqari o'rganish ham muhimligini" in md
    assert "p3" in md
    assert "## dropped" in md and "bad_kind" in md
    assert "<" not in md.replace("<!--", "")


def test_compare_md_counts(essay, fake_raw):
    result = extract.build_result(essay, "haiku", fake_raw)
    md = extract.render_compare([result])
    assert "149_qiziquvchanlik" in md and "haiku" in md
    assert "person 1" in md and "recommends 1" in md and "quote_not_found 2" in md


# --- run + raw response cache ---


def test_run_saves_outputs_and_second_run_uses_cache(tmp_path, fake_raw):
    data = tmp_path / "data"
    (data / "essays_md").mkdir(parents=True)
    (data / "essays_md" / "149_qiziquvchanlik.md").write_text(ESSAY_MD, encoding="utf-8")
    out = tmp_path / "extract"

    client = FakeClient(fake_raw)
    first = extract.run_one(data / "essays_md" / "149_qiziquvchanlik.md", "haiku", out, client, force=False)
    assert len(client.calls) == 1
    call = client.calls[0]
    assert call["model"] == "claude-haiku-5-5"
    assert call["output_format"] is extract.Extraction
    assert (out / "raw" / "haiku" / "149_qiziquvchanlik.json").exists()
    assert (out / "haiku" / "149_qiziquvchanlik.json").exists()
    assert (out / "haiku" / "149_qiziquvchanlik.review.md").exists()

    second = extract.run_one(data / "essays_md" / "149_qiziquvchanlik.md", "haiku", out, NoNetworkClient(), force=False)
    assert second == first


def test_find_essays_by_number(tmp_path):
    md = tmp_path / "essays_md"
    md.mkdir()
    for name in ("002_daraxt.md", "149_qiziquvchanlik.md", "180_mimetik.md", "181_x.md"):
        (md / name).write_text("", encoding="utf-8")
    assert [p.name for p in extract.find_essays(tmp_path, [2, 180])] == ["002_daraxt.md", "180_mimetik.md"]
    with pytest.raises(SystemExit):
        extract.find_essays(tmp_path, [7])


def test_run_all_aborts_on_first_authentication_error(tmp_path):
    import anthropic
    import httpx

    data = tmp_path / "data"
    (data / "essays_md").mkdir(parents=True)
    paths = []
    for name in ("002_a.md", "149_qiziquvchanlik.md"):
        (data / "essays_md" / name).write_text(ESSAY_MD.replace("number: 149", f"number: {int(name[:3])}"), encoding="utf-8")
        paths.append(data / "essays_md" / name)

    class AuthFailClient:
        calls = 0

        @property
        def messages(self):
            return self

        def parse(self, **kwargs):
            AuthFailClient.calls += 1
            response = httpx.Response(401, request=httpx.Request("POST", "https://api.anthropic.com/v1/messages"))
            raise anthropic.AuthenticationError("invalid x-api-key", response=response, body=None)

    with pytest.raises(SystemExit) as exc:
        extract.run_all(paths, ["haiku", "sonnet"], tmp_path / "extract", AuthFailClient(), force=False)
    assert exc.value.code == 1
    assert AuthFailClient.calls == 1


# --- cli backend (claude -p on the subscription) ---

import os
import subprocess


def _cli_stdout(result_text, is_error=False, model="claude-haiku-5-5"):
    return json.dumps({
        "type": "result", "subtype": "success", "is_error": is_error, "result": result_text,
        "duration_ms": 12345, "total_cost_usd": 0.0123,
        "usage": {"input_tokens": 10, "cache_creation_input_tokens": 2990, "cache_read_input_tokens": 0, "output_tokens": 1500},
        "modelUsage": {model: {}},
    })


@pytest.fixture
def essay_file(tmp_path):
    md = tmp_path / "data" / "essays_md"
    md.mkdir(parents=True)
    path = md / "149_qiziquvchanlik.md"
    path.write_text(ESSAY_MD, encoding="utf-8")
    return path


@pytest.fixture
def fake_cli(monkeypatch):
    for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_BASE"):
        monkeypatch.setenv(var, "sk-or-v1-should-not-leak")
    calls = []
    state = {"stdout": None, "returncode": 0}

    def run(args, input=None, capture_output=None, text=None, env=None, cwd=None, timeout=None):
        calls.append({"args": args, "input": input, "env": env, "cwd": cwd, "cwd_listing": os.listdir(cwd)})
        return subprocess.CompletedProcess(args, state["returncode"], stdout=state["stdout"], stderr="")

    monkeypatch.setattr(extract.subprocess, "run", run)
    return calls, state


def test_cli_call_cleans_env_and_isolates(essay_file, tmp_path, fake_raw, fake_cli):
    calls, state = fake_cli
    state["stdout"] = _cli_stdout(extract.response_text(fake_raw))
    result = extract.run_one(essay_file, "haiku", tmp_path / "extract", None, force=False, backend="cli")

    call = calls[0]
    for var in ("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_BASE"):
        assert var not in call["env"]
    assert "PATH" in call["env"]
    args = call["args"]
    assert args[0] == "claude" and "-p" in args
    assert args[args.index("--model") + 1] == "claude-haiku-5-5"
    assert args[args.index("--output-format") + 1] == "json"
    assert args[args.index("--tools") + 1] == ""
    assert args[args.index("--setting-sources") + 1] == ""
    assert args[args.index("--system-prompt") + 1] == extract.SYSTEM
    for flag in ("--strict-mcp-config", "--disable-slash-commands", "--no-session-persistence"):
        assert flag in args
    assert call["cwd_listing"] == [] and not str(call["cwd"]).startswith(str(Path(__file__).parent))
    assert "[p1] Qiziquvchanlik muallifni hayron qoldiradi" in call["input"]
    assert '"relations"' in call["input"]  # the json schema is in the prompt

    assert len(result["relations"]) == 4
    assert result["backend"] == "cli" and result["billed"] is False
    assert result["usage"] == {"input_tokens": 3000, "output_tokens": 1500}
    assert result["duration_ms"] == 12345 and result["cost_usd"] == 0.0123


def test_cli_compare_marks_subscription(essay_file, tmp_path, fake_raw, fake_cli):
    calls, state = fake_cli
    state["stdout"] = _cli_stdout(extract.response_text(fake_raw))
    result = extract.run_one(essay_file, "haiku", tmp_path / "extract", None, force=False, backend="cli")
    md = extract.render_compare([result])
    assert "subscription, not billed" in md and "12.3 s" in md


@pytest.mark.parametrize("text", [
    "Here is the graph: {}",
    '```json\n{"entities": [], "relations": []}\n```',
    '{"entities": []}',
    '{"entities": [{"name": "x"}], "relations": []}',
])
def test_cli_bad_json_is_an_error_without_retry(essay_file, tmp_path, fake_cli, text, capsys):
    calls, state = fake_cli
    state["stdout"] = _cli_stdout(text)
    results, failures = extract.run_all([essay_file], ["haiku"], tmp_path / "extract", None, force=False, backend="cli")
    assert results == []
    assert failures == [("149_qiziquvchanlik", "haiku", "bad_json")]
    assert len(calls) == 1
    assert "bad_json" in capsys.readouterr().err


def test_cli_error_result_is_an_error_not_bad_json(essay_file, tmp_path, fake_cli):
    calls, state = fake_cli
    state["stdout"] = _cli_stdout("Invalid API key", is_error=True)
    state["returncode"] = 1
    results, failures = extract.run_all([essay_file], ["haiku"], tmp_path / "extract", None, force=False, backend="cli")
    assert results == [] and failures == [("149_qiziquvchanlik", "haiku", "cli_error")]


def test_backend_flag_defaults_to_cli():
    assert extract.parse_args([]).backend == "cli"
    assert extract.parse_args(["--backend", "sdk"]).backend == "sdk"


# --- non-breaking spaces (U+00A0 from &nbsp;) read as normal spaces ---


def test_plain_text_maps_nbsp_to_space():
    assert extract.plain_text("professional xatokor deb") == "professional xatokor deb"
    assert extract.plain_text("Shoushenkdan qochish  filmidagi") == "Shoushenkdan qochish filmidagi"


def test_nbsp_mapping_leaves_apostrophes_untouched():
    s = "o‘g‘il oʻzbek o'g'il"
    assert extract.plain_text(s) == "o‘g‘il oʻzbek o'g'il"


def test_quote_with_normal_space_matches_nbsp_paragraph():
    md = ESSAY_MD.replace("Charli Manger **sohadan tashqari", "Charli Manger **sohadan tashqari")
    assert md.count(" ") == 2
    essay = extract.parse_essay(md)
    assert extract.check_quote(essay, "p3", "Charli Manger sohadan tashqari o'rganish") is None
    assert " " not in extract.build_prompt(essay)


# --- round 2: counterexample_of, whole-sentence quotes, base_name, sonnet default ---


def test_seven_kinds_with_counterexample_of():
    assert extract.RELATION_KINDS == [
        "wrote", "recommends", "criticises", "inspired_by", "example_of", "counterexample_of", "associated_with",
    ]
    assert "counterexample_of" in extract.Relation.model_json_schema()["properties"]["kind"]["description"]
    assert "counterexample_of" in extract.SYSTEM


def test_prompt_asks_for_base_name():
    assert "base_name" in extract.SYSTEM  # the quote rule moved to 1-3 sentences in round 3


def test_base_name_is_required_and_kept(essay, fake_raw):
    assert "base_name" in extract.Entity.model_json_schema()["required"]
    result = extract.build_result(essay, "sonnet", fake_raw)
    assert [e["base_name"] for e in result["entities"]] == ["Charli Manger", "Qiziquvchanlik", "Berkshir"]


def test_review_shows_base_name_only_when_it_differs(essay, fake_raw):
    result = extract.build_result(essay, "sonnet", fake_raw)
    result["entities"][0] = {**result["entities"][0], "name": "janob Mangerda", "base_name": "Manger"}
    md = extract.render_review(result)
    assert "**janob Mangerda** → Manger" in md
    assert "**Qiziquvchanlik**:" in md and "→ Qiziquvchanlik:" not in md


def test_missing_base_name_is_bad_json(essay, fake_raw):
    import copy
    raw = copy.deepcopy(fake_raw)
    blk = next(b for b in raw["content"] if b["type"] == "text")
    d = json.loads(blk["text"])
    del d["entities"][0]["base_name"]
    blk["text"] = json.dumps(d)
    with pytest.raises(extract.BadJson):
        extract.build_result(essay, "sonnet", raw)


def test_model_defaults_to_sonnet():
    assert extract.parse_args([]).model == "sonnet"
    assert extract.parse_args(["--model", "haiku"]).model == "haiku"


# --- round 3: multi-sentence quotes, every person/work linked, name kept as written ---


def test_quote_of_consecutive_sentences_in_one_paragraph_passes(essay):
    two = "O'rganishdan to'xtamaydigan odamlar. Angliyada yashaydigan vatandoshimiz shuni kuzatgan."
    assert extract.check_quote(essay, "p2", two) is None


def test_quote_spanning_two_paragraphs_fails(essay):
    across = "vatandoshimiz shuni kuzatgan. Shuning uchun Charli Manger"
    assert extract.check_quote(essay, "p2", across) == "quote_not_found"
    assert extract.check_quote(essay, "p3", across) == "quote_not_found"


def test_prompt_round3_rules():
    assert "1-3 consecutive sentences" in extract.SYSTEM
    assert "at least one relation" in extract.SYSTEM
    assert "lowercase" in extract.SYSTEM


def test_unlinked_counts_only_person_and_work(essay, fake_raw):
    result = extract.build_result(essay, "sonnet", fake_raw)
    assert result["unlinked"] == []  # Manger is linked; idea/organization never count

    only_author = [r for r in result["relations"] if r["source"] == extract.AUTHOR]
    unlinked = extract.find_unlinked(result["entities"], only_author)
    assert unlinked == ["Charli Manger"]


def test_link_to_author_counts_as_linked():
    ents = [{"name": "Kitob", "type": "work"}, {"name": "Ali", "type": "person"}]
    rels = [{"source": extract.AUTHOR, "target": "Kitob"}]
    assert extract.find_unlinked(ents, rels) == ["Ali"]


def test_unlinked_in_review_and_compare(essay, fake_raw):
    result = extract.build_result(essay, "sonnet", fake_raw)
    result["unlinked"] = ["Ben Grem", "Pol Getti"]
    review = extract.render_review(result)
    assert review.index("## unlinked") > review.index("## dropped")
    assert "- Ben Grem" in review and "- Pol Getti" in review
    compare = extract.render_compare([result])
    assert "| unlinked |" in compare and "| 2 (Ben Grem, Pol Getti) |" in compare


# --- task 03 step 1: associated_with only as a last resort ---


def test_prompt_makes_associated_with_a_last_resort():
    assert "associated_with only when none of the other 6 kinds fits" in extract.SYSTEM
    assert "inspired_by" in extract.SYSTEM.split("associated_with only when")[1].split("\n- ")[0]
    assert "recommends" in extract.SYSTEM.split("associated_with only when")[1].split("\n- ")[0]


# --- task 03 step 2: all essays, --jobs, clean stop on cli_error ---

import threading
import time


def _essay_dir(tmp_path, numbers):
    md = tmp_path / "essays_md"
    md.mkdir(exist_ok=True)
    for n in numbers:
        (md / f"{n:03d}_e{n}.md").write_text("", encoding="utf-8")
    return tmp_path


def test_essay_selection_all_and_range(tmp_path):
    data = _essay_dir(tmp_path, [2, 3, 10, 149])
    assert [p.name for p in extract.select_paths(data, "all")] == ["002_e2.md", "003_e3.md", "010_e10.md", "149_e149.md"]
    assert [p.name for p in extract.select_paths(data, "3-10")] == ["003_e3.md", "010_e10.md"]
    assert [p.name for p in extract.select_paths(data, "2,149")] == ["002_e2.md", "149_e149.md"]


class FakeRunOne:
    """Stands in for run_one: records calls, fails on chosen essays, can be slow."""

    def __init__(self, fail=None, delay=0.0):
        self.fail = fail or {}
        self.delay = delay
        self.calls = []
        self.lock = threading.Lock()

    def __call__(self, path, alias, out_dir, client, force, backend="sdk"):
        with self.lock:
            self.calls.append(path.stem)
        time.sleep(self.delay)
        exc = self.fail.get(path.stem)
        if exc:
            raise exc
        return {"essay": {"id": path.stem}, "alias": alias, "entities": [], "relations": [], "dropped": [],
                "duration_ms": 1, "cost_usd": 0.0, "billed": False}


def test_jobs_keep_sequential_order(tmp_path, monkeypatch):
    data = _essay_dir(tmp_path, range(1, 10))
    fake = FakeRunOne(delay=0.01)
    monkeypatch.setattr(extract, "run_one", fake)
    paths = extract.select_paths(data, "all")
    results, failures = extract.run_all(paths, ["sonnet"], tmp_path / "x", None, False, "cli", jobs=3)
    assert [r["essay"]["id"] for r in results] == [p.stem for p in paths]
    assert failures == [] and sorted(fake.calls) == [p.stem for p in paths]


def test_cli_error_stops_new_calls_and_lets_running_finish(tmp_path, monkeypatch):
    data = _essay_dir(tmp_path, range(1, 21))
    fake = FakeRunOne(fail={"002_e2": extract.CliError("usage limit reached")}, delay=0.05)
    monkeypatch.setattr(extract, "run_one", fake)
    paths = extract.select_paths(data, "all")
    results, failures = extract.run_all(paths, ["sonnet"], tmp_path / "x", None, False, "cli", jobs=3)
    assert ("002_e2", "sonnet", "cli_error") in failures
    not_started = [f for f in failures if f[2] == "not_started"]
    assert len(fake.calls) <= 4 + 1          # the 3 running at the time plus at most one picked up
    assert len(results) + len([f for f in failures if f[2] == "cli_error"]) + len(not_started) == 20
    assert len(not_started) >= 15


def test_cli_error_sequential_stops_right_after(tmp_path, monkeypatch):
    data = _essay_dir(tmp_path, range(1, 6))
    fake = FakeRunOne(fail={"002_e2": extract.CliError("limit")})
    monkeypatch.setattr(extract, "run_one", fake)
    results, failures = extract.run_all(extract.select_paths(data, "all"), ["sonnet"], tmp_path / "x", None,
                                        False, "cli", jobs=1)
    assert fake.calls == ["001_e1", "002_e2"]
    assert [f[0] for f in failures if f[2] == "not_started"] == ["003_e3", "004_e4", "005_e5"]


def test_bad_json_does_not_stop_the_run(tmp_path, monkeypatch):
    data = _essay_dir(tmp_path, range(1, 5))
    fake = FakeRunOne(fail={"002_e2": extract.BadJson("relations missing")})
    monkeypatch.setattr(extract, "run_one", fake)
    results, failures = extract.run_all(extract.select_paths(data, "all"), ["sonnet"], tmp_path / "x", None,
                                        False, "cli", jobs=2)
    assert failures == [("002_e2", "sonnet", "bad_json")] and len(results) == 3


def test_jobs_flag():
    assert extract.parse_args([]).jobs == 1
    assert extract.parse_args(["--jobs", "3", "--essays", "all"]).jobs == 3


# --- task 03: link endpoints resolve by name or base_name, case-insensitively ---


def _raw_from(entities, relations):
    return {"model": "claude-sonnet-5-5", "stop_reason": "end_turn", "usage": {"input_tokens": 1, "output_tokens": 1},
            "content": [{"type": "text", "text": json.dumps({"entities": entities, "relations": relations},
                                                            ensure_ascii=False)}]}


def _ent(name, base, etype="idea", paragraphs=("p3",)):
    return {"name": name, "base_name": base, "type": etype, "description": "d", "aliases": [],
            "paragraphs": list(paragraphs)}


def _rel(source, target, kind="example_of"):
    return {"source": source, "target": target, "kind": kind, "label": "l", "paragraph": "p3",
            "quote": "sohadan tashqari o'rganish ham muhimligini"}


def test_endpoint_matching_ignores_case_and_keeps_entity_name(essay):
    raw = _raw_from([_ent("Charli Manger", "Charli Manger", "person"), _ent("blog yuritish", "Blog yuritish")],
                    [_rel("charli manger", "Blog Yuritish")])
    r = extract.build_result(essay, "sonnet", raw)
    assert r["dropped"] == []
    assert (r["relations"][0]["source"], r["relations"][0]["target"]) == ("Charli Manger", "blog yuritish")
    assert r["unlinked"] == []


def test_endpoint_matching_uses_base_name(essay):
    raw = _raw_from([_ent("janob Taleb", "Taleb", "person"), _ent("noyob tajriba", "Noyob tajriba")],
                    [_rel("Taleb", "noyob tajriba", "recommends")])
    r = extract.build_result(essay, "sonnet", raw)
    assert r["dropped"] == [] and r["relations"][0]["source"] == "janob Taleb"


def test_author_matches_case_insensitively(essay):
    raw = _raw_from([_ent("ego", "Ego")], [_rel("aziz rahimov", "ego", "criticises")])
    r = extract.build_result(essay, "sonnet", raw)
    assert r["dropped"] == [] and r["relations"][0]["source"] == extract.AUTHOR


def test_true_unknown_still_drops(essay):
    raw = _raw_from([_ent("ego", "Ego")], [_rel("Antoniy", "ego")])
    r = extract.build_result(essay, "sonnet", raw)
    assert [d["reason"] for d in r["dropped"]] == ["unknown_entity"] and r["relations"] == []


def test_ambiguous_lowercase_match_drops_instead_of_guessing(essay):
    raw = _raw_from([_ent("Ego", "Ego"), _ent("EGO", "Ego kitobi", "work")], [_rel("ego", "Ego kitobi")])
    r = extract.build_result(essay, "sonnet", raw)
    assert [d["reason"] for d in r["dropped"]] == ["unknown_entity"]


def test_exact_name_wins_over_an_ambiguous_lowercase_form(essay):
    raw = _raw_from([_ent("Ego", "Ego"), _ent("EGO", "Ego kitobi", "work")], [_rel("EGO", "Ego")])
    r = extract.build_result(essay, "sonnet", raw)
    assert r["dropped"] == [] and (r["relations"][0]["source"], r["relations"][0]["target"]) == ("EGO", "Ego")


def test_offline_never_calls_and_reports_missing_raw(tmp_path, fake_raw):
    data = tmp_path / "data"
    (data / "essays_md").mkdir(parents=True)
    path = data / "essays_md" / "149_qiziquvchanlik.md"
    path.write_text(ESSAY_MD, encoding="utf-8")
    out = tmp_path / "extract"
    results, failures = extract.run_all([path], ["sonnet"], out, NoNetworkClient(), False, "cli", offline=True)
    assert results == [] and failures == [("149_qiziquvchanlik", "sonnet", "no_raw")]

    (out / "raw" / "sonnet").mkdir(parents=True)
    (out / "raw" / "sonnet" / "149_qiziquvchanlik.json").write_text(json.dumps(fake_raw), encoding="utf-8")
    results, failures = extract.run_all([path], ["sonnet"], out, NoNetworkClient(), True, "cli", offline=True)
    assert failures == [] and len(results) == 1  # --force is ignored offline: the cached answer is used


def test_offline_flag():
    assert extract.parse_args([]).offline is False
    assert extract.parse_args(["--offline", "--essays", "all"]).offline is True


# --- task 07: urls from links ---

LINKS_MD = """\
---
number: 7
slug: havolalar
title: "Havolalar"
author: Aziz Rahimov
source: https://parallelmuhit.uz/havolalar
---

Shahboz bilan suhbatga [qarang](https://youtu.be/abc). Rasm: ![alt](https://b.x/i.jpg) va [pochta](mailto:a@b.uz) hamda [yana](https://youtu.be/abc) va [Atomic Habits](https://example.com/ah "sarlavha").

![](https://b.x/only.jpg)

Havolasiz paragraf.
"""


def test_parse_essay_returns_http_links_only_deduped_in_order():
    e = extract.parse_essay(LINKS_MD)
    p1 = e["paragraphs"][0]
    assert p1["links"] == [{"text": "qarang", "url": "https://youtu.be/abc"},
                           {"text": "Atomic Habits", "url": "https://example.com/ah"}]
    assert e["paragraphs"][1]["links"] == []


def test_links_do_not_change_paragraph_ids_or_text():
    e = extract.parse_essay(LINKS_MD)
    assert [p["id"] for p in e["paragraphs"]] == ["p1", "p2"]
    assert e["paragraphs"][0]["text"] == (
        "Shahboz bilan suhbatga qarang. Rasm: va pochta hamda yana va Atomic Habits.")
