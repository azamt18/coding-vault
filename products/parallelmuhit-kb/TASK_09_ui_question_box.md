# task 09: question box in the graph ui (draft, needs the user's ok)

written 2026-11-12 by the plan session. follows task 08 (`ask.py`, `retrieve.py`).

## goal

the user types an uzbek question in the ui and sees the answer with the checked citations, quotes and urls. clicking a cited paragraph focuses its essay or entity node in the graph.

## design (recommended defaults)

1. **local server `serve.py`** (stdlib `http.server`, no new dependency): `POST /api/ask {question}` → the same dict `ask.ask()` returns, as json. it loads corpus, bm25 and graph once at start. `claude -p` runs per request, one at a time (a lock), because the subscription limit is shared.
2. **dev wiring:** vite proxies `/api` to the server (`vite.config.ts`). the static build still works without the server, and the box is then hidden (a failed `/api/health` hides it).
3. **ui:** a panel with a text box, a "thinking" state, the answer text, the citations list. each `[id#pN]` in the answer is a link that focuses the essay node and shows the quote.
4. **no change to answer rules:** citation checking stays in `ask.py`. the ui renders what the server returns and never trusts model text for quotes or urls.
5. **tests:** server handler tested with a fake `generate` (valid question, empty question → 400, model error → 502 with a one-line message); ui test for the render of an answer with a dropped citation.

## not in scope

- publishing (the later static site has no server, so the box stays local-only).
- streaming answers, chat history, embeddings.

## done when

`python3 serve.py` + `npm run dev` in `ui/` answers a live question, a click on a citation focuses the node, and all python and npm tests pass.
