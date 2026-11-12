"""Tests for serve.py: offline, the model is an injected function."""

import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

import ask
import extract
import retrieve
import serve
from test_retrieve import LINKS, NODES, PARS


def service(generate):
    corpus = {p["id"]: p for p in PARS}
    return serve.Service(corpus, retrieve.BM25(PARS), NODES, LINKS, generate)


def body(**kw):
    return json.dumps(kw).encode()


def test_valid_question_returns_the_ask_dict():
    status, out = service(lambda s, p: "Taleb yozadi [001_a#p1].").ask(body(question="Taleb haqida nima deydi?"))
    assert status == 200
    assert out["citations"][0]["id"] == "001_a#p1" and out["flagged"] is False
    assert set(out) == {"question", "answer", "dropped", "citations", "flagged"}


@pytest.mark.parametrize("raw", [body(question=""), body(question="   "), body(), b"not json", b"[]", body(question=5)])
def test_bad_question_is_400_and_never_calls_the_model(raw):
    def boom(s, p):
        raise AssertionError("model called")
    status, out = service(boom).ask(raw)
    assert status == 400 and "error" in out


def test_model_error_is_502_with_a_one_line_message():
    def fail(s, p):
        raise extract.CliError("exit 1: rate limit\nsecond line")
    status, out = service(fail).ask(body(question="Taleb?"))
    assert status == 502
    assert "\n" not in out["error"] and "rate limit" in out["error"]


def test_too_long_question_is_400():
    status, _ = service(lambda s, p: "x").ask(body(question="a" * (serve.MAX_QUESTION + 1)))
    assert status == 400


def test_requests_run_one_at_a_time():
    active, peak = [0], [0]
    gate = threading.Lock()

    def gen(s, p):
        with gate:
            active[0] += 1
            peak[0] = max(peak[0], active[0])
        import time
        time.sleep(0.05)
        with gate:
            active[0] -= 1
        return "Taleb [001_a#p1]."
    svc = service(gen)
    ts = [threading.Thread(target=svc.ask, args=(body(question="Taleb?"),)) for _ in range(4)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert peak[0] == 1


@pytest.fixture
def live():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), serve.make_handler(service(lambda s, p: "Taleb [001_a#p1].")))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()


def post(url, data):
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.load(e)


def test_http_health_ask_and_unknown_route(live):
    with urllib.request.urlopen(live + "/api/health") as r:
        assert r.status == 200 and json.load(r) == {"ok": True}
    assert post(live + "/api/ask", body(question="Taleb?"))[0] == 200
    assert post(live + "/api/ask", body(question=""))[0] == 400
    assert post(live + "/api/nope", b"{}")[0] == 404
