import { describe, expect, it } from "vitest";
import { fold, search } from "./search";
import { fixture } from "./fixture";

describe("fold", () => {
  it("casefolds and drops every apostrophe form", () => {
    for (const s of ["O‘qish", "Oʻqish", "O'qish", "O’qish", "O`qish", "Oʼqish"]) {
      expect(fold(s)).toBe("oqish");
    }
  });

  it("trims and collapses spaces", () => {
    expect(fold("  Charli   Manger ")).toBe("charli manger");
  });
});

describe("search", () => {
  const nodes = fixture().nodes;

  it("matches aliases", () => {
    const hits = search(nodes, "munger");
    expect(hits.map((n) => n.id)).toEqual(["person:munger"]);
  });

  it("ignores apostrophe form and case", () => {
    expect(search(nodes, "O'QISH").map((n) => n.id)).toEqual(["idea:o'qish"]);
  });

  it("ranks an exact label match before a substring match", () => {
    const hits = search(nodes, "kitob");
    expect(hits[0].id).toBe("work:kitob");
  });

  it("returns nothing for an empty query", () => {
    expect(search(nodes, "  ")).toEqual([]);
  });

  it("honours the limit", () => {
    expect(search(nodes, "a", 2)).toHaveLength(2);
  });
});
