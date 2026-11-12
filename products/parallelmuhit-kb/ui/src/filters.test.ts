import { describe, expect, it } from "vitest";
import { defaultFilters, visible, type Filters } from "./filters";
import { fixture } from "./fixture";

const g = fixture();
const all = (): Filters => ({
  types: new Set(g.nodes.map((n) => n.type)),
  kinds: new Set(g.links.map((l) => l.kind)),
  essay: null,
});
const linkIdx = (v: ReturnType<typeof visible>) => [...v.links].sort((a, b) => a - b);

describe("defaultFilters", () => {
  it("hides essays, wrote and mentioned_in, keeps the rest", () => {
    const f = defaultFilters();
    expect(f.types.has("essay")).toBe(false);
    expect(f.kinds.has("wrote")).toBe(false);
    expect(f.kinds.has("mentioned_in")).toBe(false);
    for (const t of ["person", "work", "idea", "organization", "theme", "author"]) expect(f.types.has(t)).toBe(true);
    for (const k of ["recommends", "criticises", "inspired_by", "example_of", "counterexample_of", "associated_with", "in_theme"])
      expect(f.kinds.has(k)).toBe(true);
    expect(f.essay).toBeNull();
  });
});

describe("visible", () => {
  it("with everything on, shows every node and every link (weak links too)", () => {
    const v = visible(g, all());
    expect(v.nodes.size).toBe(g.nodes.length);
    expect(v.links.size).toBe(g.links.length);
  });

  it("a kind filter hides only links of that kind", () => {
    const f = all();
    f.kinds.delete("criticises");
    const v = visible(g, f);
    expect(linkIdx(v)).toEqual([0, 1, 2, 3, 5]);
    expect(v.nodes.size).toBe(g.nodes.length);
  });

  it("a type filter hides those nodes and every link touching them", () => {
    const f = all();
    f.types.delete("work");
    const v = visible(g, f);
    expect(v.nodes.has("work:kitob")).toBe(false);
    expect(linkIdx(v)).toEqual([0, 1, 2, 5]);
  });

  it("an essay filter keeps only that essay's links and the nodes they touch", () => {
    const f = all();
    f.essay = "002_b";
    const v = visible(g, f);
    expect(linkIdx(v)).toEqual([3, 4]);
    expect([...v.nodes].sort()).toEqual(["idea:o'qish", "person:munger", "work:kitob"]);
  });

  it("combined filters give the intersection", () => {
    const f = all();
    f.essay = "002_b";
    f.kinds.delete("criticises");
    f.types.delete("person");
    const v = visible(g, f);
    expect(linkIdx(v)).toEqual([3]);
    expect([...v.nodes].sort()).toEqual(["idea:o'qish", "work:kitob"]);
  });

  it("defaults hide essay nodes and wrote/mentioned_in links", () => {
    const v = visible(g, defaultFilters());
    expect(v.nodes.has("essay:001_a")).toBe(false);
    expect(linkIdx(v)).toEqual([2, 3, 4, 5]);
  });
});
