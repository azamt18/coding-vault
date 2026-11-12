import "./style.css";
import { MultiDirectedGraph } from "graphology";
import Sigma from "sigma";
import FA2Layout from "graphology-layout-forceatlas2/worker";
import { inferSettings } from "graphology-layout-forceatlas2";
import { LINK_KINDS, NODE_TYPES, loadGraph, type KbGraph, type KbLink, type KbNode } from "./data";
import { defaultFilters, visible, type Filters, type Visible } from "./filters";
import { neighbourhood } from "./focus";
import { search } from "./search";
import { urlItems, type KbUrl } from "./urls";
import { answerView, essayNodeId, type AskResult } from "./answer";
import { DIM_EDGE, DIM_NODE, KIND_COLOR, TYPE_COLOR } from "./colors";

const LAYOUT_MS = 8000;
const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;

function el<K extends keyof HTMLElementTagNameMap>(
  tag: K, props: Partial<HTMLElementTagNameMap[K]> = {}, ...kids: (Node | string)[]
): HTMLElementTagNameMap[K] {
  const e = Object.assign(document.createElement(tag), props);
  e.append(...kids);
  return e;
}

// deterministic start positions so every load lays out the same way
function hash(s: string, seed: number): number {
  let h = seed;
  for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 2654435761);
  return ((h >>> 0) % 10000) / 10000;
}

function buildGraph(kb: KbGraph) {
  const g = new MultiDirectedGraph();
  const degree = new Map<string, number>();
  for (const l of kb.links) {
    degree.set(l.source, (degree.get(l.source) ?? 0) + 1);
    degree.set(l.target, (degree.get(l.target) ?? 0) + 1);
  }
  for (const n of kb.nodes) {
    const weight = n.mention_count ?? degree.get(n.id) ?? 1; // essays/themes/author: by degree
    g.addNode(n.id, {
      label: n.label,
      kbType: n.type, // "type" is reserved by sigma for the render program
      size: Math.min(16, 2 + 1.6 * Math.sqrt(weight)), // capped so the author/essays do not swamp the view
      color: TYPE_COLOR[n.type] ?? "#000",
      x: hash(n.id, 1) * 100,
      y: hash(n.id, 2) * 100,
    });
  }
  kb.links.forEach((l, i) => {
    // the essay-structure links pull less, so the layout groups by meaning, not by essay
    const weak = l.kind === "mentioned_in" || l.kind === "wrote";
    g.addDirectedEdgeWithKey(`e${i}`, l.source, l.target, {
      idx: i, kind: l.kind, color: KIND_COLOR[l.kind] ?? "#999", size: 1, weight: weak ? 0.1 : 1,
    });
  });
  return g;
}

async function main() {
  const kb = await loadGraph();
  const byId = new Map(kb.nodes.map((n) => [n.id, n]));
  const linksOf = new Map<string, number[]>();
  kb.links.forEach((l, i) => {
    for (const end of [l.source, l.target]) {
      if (!linksOf.has(end)) linksOf.set(end, []);
      linksOf.get(end)!.push(i);
    }
  });

  const graph = buildGraph(kb);
  const filters: Filters = defaultFilters();
  let vis: Visible = visible(kb, filters);
  let selected: string | null = null;
  let focus: Set<string> | null = null;

  const renderer = new Sigma(graph, $("stage"), {
    defaultEdgeType: "arrow",
    labelRenderedSizeThreshold: 7,
    zIndex: true,
    nodeReducer: (id, d) => {
      if (!vis.nodes.has(id) && id !== selected) return { ...d, hidden: true };
      if (focus && !focus.has(id)) return { ...d, color: DIM_NODE, label: "", zIndex: 0 };
      if (id === selected) return { ...d, highlighted: true, zIndex: 2 };
      return { ...d, zIndex: focus ? 1 : 0 };
    },
    edgeReducer: (_id, d) => {
      if (!vis.links.has(d.idx)) return { ...d, hidden: true };
      if (focus) {
        const l = kb.links[d.idx];
        if (l.source !== selected && l.target !== selected) return { ...d, color: DIM_EDGE, zIndex: 0 };
        return { ...d, size: 2, zIndex: 1 };
      }
      return d;
    },
  });

  // layout runs in a web worker for a few seconds, then stops; the button toggles it
  const layout = new FA2Layout(graph, {
    settings: { ...inferSettings(graph), barnesHutOptimize: true, edgeWeightInfluence: 1 },
    getEdgeWeight: "weight",
  });
  const layoutBtn = $<HTMLButtonElement>("layout");
  const setLayout = (on: boolean) => {
    if (on) layout.start(); else layout.stop();
    layoutBtn.textContent = on ? "layout: running" : "layout: stopped";
  };
  setLayout(true);
  setTimeout(() => setLayout(false), LAYOUT_MS);
  layoutBtn.onclick = () => setLayout(!layout.isRunning());

  function refresh() {
    vis = visible(kb, filters);
    focus = selected ? neighbourhood(kb.links, selected, vis.links) : null;
    $("count").textContent = `${vis.nodes.size} nodes, ${vis.links.size} links shown`;
    renderer.refresh({ skipIndexation: true });
  }

  function select(id: string | null, centre = false) {
    selected = id;
    renderDetails();
    refresh();
    if (id && centre) {
      const d = renderer.getNodeDisplayData(id);
      if (d) renderer.getCamera().animate({ x: d.x, y: d.y, ratio: 0.25 }, { duration: 500 });
    }
  }

  // --- controls ---
  const count = <T,>(xs: T[], key: (x: T) => string) =>
    xs.reduce((m, x) => m.set(key(x), (m.get(key(x)) ?? 0) + 1), new Map<string, number>());
  const typeCount = count(kb.nodes, (n) => n.type);
  const kindCount = count(kb.links, (l) => l.kind);

  function checkboxes(box: HTMLElement, names: readonly string[], on: Set<string>, colors: Record<string, string>,
    counts: Map<string, number>, line: boolean) {
    for (const name of names) {
      const input = el("input", { type: "checkbox", checked: on.has(name) });
      input.onchange = () => { if (input.checked) on.add(name); else on.delete(name); refresh(); };
      const sw = el("span", { className: line ? "swatch line" : "swatch" });
      sw.style.background = colors[name];
      box.append(el("label", { className: "check" }, input, sw, name.replace(/_/g, " "),
        el("span", { className: "n" }, String(counts.get(name) ?? 0))));
    }
  }
  checkboxes($("types"), NODE_TYPES, filters.types, TYPE_COLOR, typeCount, false);
  checkboxes($("kinds"), LINK_KINDS, filters.kinds, KIND_COLOR, kindCount, true);

  const essaySel = $<HTMLSelectElement>("essay");
  for (const n of kb.nodes.filter((n) => n.type === "essay").sort((a, b) => (a.number ?? 0) - (b.number ?? 0))) {
    essaySel.append(el("option", { value: n.id.replace(/^essay:/, "") }, `${n.number} · ${n.label}`));
  }
  essaySel.onchange = () => { filters.essay = essaySel.value || null; refresh(); };

  const input = $<HTMLInputElement>("search");
  const results = $<HTMLUListElement>("results");
  input.oninput = () => {
    results.replaceChildren(...search(kb.nodes, input.value).map((n) => {
      const sw = el("span", { className: "swatch" });
      sw.style.background = TYPE_COLOR[n.type];
      const li = el("li", {}, sw, n.label, el("span", { className: "badge" }, n.type));
      li.onclick = () => { results.replaceChildren(); input.value = n.label; select(n.id, true); };
      return li;
    }));
  };

  $("clear").onclick = () => select(null);
  renderer.on("clickNode", ({ node }) => select(node));
  renderer.on("clickStage", () => select(null));

  // --- details panel ---
  function jump(id: string) {
    const n = byId.get(id)!;
    const b = el("button", { className: vis.nodes.has(id) ? "jump" : "jump hidden-node", title: n.type }, n.label);
    if (!vis.nodes.has(id)) b.title += " (hidden by filters)";
    b.onclick = () => select(id, true);
    return b;
  }

  function urlList(urls?: KbUrl[]) {
    const items = urlItems(urls);
    if (!items.length) return null;
    return el("div", { className: "urls" }, ...items.map((u) => el("a", { href: u.href, target: u.target, rel: u.rel }, u.label)));
  }

  function linkItem(l: KbLink, me: string) {
    const out = l.source === me;
    const other = out ? l.target : l.source;
    const where = [l.essay, l.paragraph ?? l.paragraphs?.join(", ")].filter(Boolean).join(" · ");
    const box = el("div", { className: "link" },
      el("div", {}, out ? "→ " : "← ", jump(other)),
      el("div", { className: "meta" }, [where, l.label].filter(Boolean).join(" — ")));
    box.style.borderLeftColor = KIND_COLOR[l.kind];
    if (l.quote) box.append(el("blockquote", {}, l.quote));
    const us = urlList(l.urls);
    if (us) box.append(us);
    return box;
  }

  function renderDetails() {
    const panel = $("node");
    if (!selected) {
      panel.className = "empty";
      panel.replaceChildren(el("p", { className: "muted" }, "click a node to see its links and quotes."));
      return;
    }
    const n: KbNode = byId.get(selected)!;
    const parts: (Node | string)[] = [
      el("h1", {}, n.label),
      el("p", { className: "muted" }, [n.type, n.mention_count ? `${n.mention_count} mentions` : ""].filter(Boolean).join(" · ")),
    ];
    if (!vis.nodes.has(n.id)) parts.push(el("p", { className: "muted" }, "hidden by the current filters."));
    if (n.source) parts.push(el("p", {}, el("a", { href: n.source, target: "_blank", rel: "noopener" }, n.source)));
    if (n.theme) parts.push(el("p", {}, "theme: ", el("strong", {}, n.theme)));
    if (n.aliases?.length) parts.push(el("h3", {}, "aliases"), el("p", {}, n.aliases.join(", ")));
    const desc = Object.entries(n.descriptions ?? {});
    if (desc.length) {
      parts.push(el("h3", {}, "descriptions"),
        el("dl", {}, ...desc.flatMap(([essay, text]) => [el("dt", {}, essay), el("dd", {}, text)])));
    }
    const nodeUrls = urlList(n.urls);
    if (nodeUrls) parts.push(el("h3", {}, "links in the essays"), nodeUrls);
    const mine = (linksOf.get(n.id) ?? []).map((i) => kb.links[i]);
    for (const kind of LINK_KINDS) {
      const ls = mine.filter((l) => l.kind === kind);
      if (!ls.length) continue;
      parts.push(el("h3", {}, `${kind.replace(/_/g, " ")} (${ls.length})`), ...ls.map((l) => linkItem(l, n.id)));
    }
    panel.className = "";
    panel.replaceChildren(...parts);
    panel.scrollTop = 0;
  }

  // --- question box: shown only when the local server (serve.py) answers /api/health ---
  const askBox = $("ask");
  fetch("/api/health").then((r) => r.ok && r.json()).then((j) => { if (j && j.ok) askBox.hidden = false; }).catch(() => {});
  const send = $<HTMLButtonElement>("send");
  const q = $<HTMLTextAreaElement>("q");
  const state = $("ask-state");
  const out = $("answer");

  function showAnswer(r: AskResult) {
    const v = answerView(r);
    const parts: Node[] = [];
    if (v.warning) parts.push(el("p", { className: "warn" }, v.warning));
    const quotes = new Map<string, HTMLElement>();
    const text = el("p", { className: "answer-text" });
    for (const s of v.segments) {
      if ("text" in s) { text.append(s.text); continue; }
      const b = el("button", { className: "jump cite" }, `[${s.cite}]`);
      b.onclick = () => {
        const node = essayNodeId(s.cite);
        if (byId.has(node)) select(node, true);
        quotes.get(s.cite)?.scrollIntoView({ block: "nearest" });
      };
      text.append(b);
    }
    parts.push(text);
    for (const c of v.citations) {
      const box = el("div", { className: "link" }, el("div", { className: "meta" }, `${c.id} · ${c.title}`),
        el("blockquote", {}, c.quote));
      const links = [
        ...(c.essayUrl ? [el("a", { href: c.essayUrl, target: "_blank", rel: "noopener noreferrer" }, "↗ essay")] : []),
        ...c.links.map((u) => el("a", { href: u.href, target: u.target, rel: u.rel }, u.label)),
      ];
      if (links.length) box.append(el("div", { className: "urls" }, ...links));
      quotes.set(c.id, box);
      parts.push(box);
    }
    out.replaceChildren(...parts);
  }

  async function ask() {
    const question = q.value.trim();
    if (!question) return;
    send.disabled = true;
    state.textContent = "thinking… (about 15 s)";
    out.replaceChildren();
    try {
      const res = await fetch("/api/ask", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question }) });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? `error ${res.status}`);
      showAnswer(data as AskResult);
      state.textContent = "";
    } catch (e) {
      state.textContent = "";
      out.replaceChildren(el("p", { className: "warn" }, String((e as Error).message ?? e)));
    } finally {
      send.disabled = false;
    }
  }
  send.onclick = ask;
  q.onkeydown = (e) => { if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) ask(); };

  refresh();
}

main().catch((err) => {
  console.error(err);
  $("stage").replaceChildren(el("p", { className: "muted", style: "padding:20px" } as any, String(err)));
});
