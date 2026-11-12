"""Local server for the ui's question box (task 09): POST /api/ask {question} -> ask.ask() as json.

stdlib only, bound to 127.0.0.1. The corpus, bm25 and graph load once at start. `claude -p` runs one request
at a time (a lock), because the subscription limit is shared. Citation checking stays in ask.py.
"""

import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import ask
import extract
import retrieve

HERE = Path(__file__).parent
MAX_QUESTION = 500
MAX_BODY = 10_000


class Service:
    def __init__(self, corpus, bm25, nodes, links, generate):
        self.args = (corpus, bm25, nodes, links)
        self.generate = generate
        self.lock = threading.Lock()

    def ask(self, raw: bytes) -> tuple[int, dict]:
        """-> (http status, json body). Never raises."""
        try:
            data = json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            return 400, {"error": "body must be json"}
        q = data.get("question") if isinstance(data, dict) else None
        if not isinstance(q, str) or not q.strip():
            return 400, {"error": "question is empty"}
        if len(q) > MAX_QUESTION:
            return 400, {"error": f"question is longer than {MAX_QUESTION} characters"}
        with self.lock:
            try:
                return 200, ask.ask(q.strip(), *self.args, generate=self.generate)
            except extract.CliError as exc:
                return 502, {"error": f"model call failed: {' '.join(str(exc).split())[:200]}"}
            except Exception as exc:  # keep the server alive; one line for the ui
                return 500, {"error": f"server error: {type(exc).__name__}"}


def make_handler(service: Service):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: int, obj: dict):
            out = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)

        def do_GET(self):
            if self.path == "/api/health":
                self._send(200, {"ok": True})
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self):
            if self.path != "/api/ask":
                return self._send(404, {"error": "not found"})
            n = int(self.headers.get("Content-Length") or 0)
            if n > MAX_BODY:
                return self._send(400, {"error": "body too large"})
            self._send(*service.ask(self.rfile.read(n)))

        def log_message(self, fmt, *args):  # quiet: questions are not logged
            pass

    return Handler


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--graph", type=Path, default=HERE / "extract" / "graph_grouped.json")
    ap.add_argument("--sonnet-dir", type=Path, default=HERE / "extract" / "sonnet")
    a = ap.parse_args(argv)
    g = json.loads(a.graph.read_text(encoding="utf-8"))
    corpus = retrieve.load_corpus(a.sonnet_dir)
    svc = Service(corpus, retrieve.BM25(list(corpus.values())), g["nodes"], g["links"], ask.cli_generate)
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(svc))
    print(f"ask server on http://127.0.0.1:{a.port}  (ctrl-c stops)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
