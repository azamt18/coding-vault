import { existsSync, readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { DATA_URL, parseGraph } from "./data";
import { fixture } from "./fixture";

const REAL = new URL("../../extract/graph_grouped.json", import.meta.url);

describe("parseGraph", () => {
  it("accepts a well-formed graph", () => {
    const g = parseGraph(fixture());
    expect(g.nodes).toHaveLength(7);
    expect(g.links).toHaveLength(6);
  });

  it("rejects a link whose endpoint is not a node", () => {
    const raw = fixture();
    raw.links.push({ source: "person:munger", target: "idea:missing", kind: "recommends" });
    expect(() => parseGraph(raw)).toThrow(/idea:missing/);
  });

  it("rejects input without nodes and links arrays", () => {
    expect(() => parseGraph({ nodes: [] })).toThrow();
    expect(() => parseGraph(null)).toThrow();
  });

  it("rejects duplicate node ids", () => {
    const raw = fixture();
    raw.nodes.push({ id: "theme:bilim", label: "x", type: "theme" });
    expect(() => parseGraph(raw)).toThrow(/theme:bilim/);
  });

  it("loads from a single path constant", () => {
    expect(DATA_URL).toBe("/graph_grouped.json");
  });
});

describe("smoke: real graph_grouped.json", () => {
  it.skipIf(!existsSync(REAL))("parses and every link endpoint is a node id", () => {
    const g = parseGraph(JSON.parse(readFileSync(REAL, "utf8")));
    const ids = new Set(g.nodes.map((n) => n.id));
    expect(g.nodes.length).toBeGreaterThan(1000);
    for (const l of g.links) {
      expect(ids.has(l.source)).toBe(true);
      expect(ids.has(l.target)).toBe(true);
    }
  });
});
