import { describe, expect, it } from "vitest";
import { neighbourhood } from "./focus";
import { fixture } from "./fixture";

const g = fixture();

describe("neighbourhood", () => {
  it("is the node plus its direct neighbours, both directions", () => {
    const n = neighbourhood(g.links, "idea:o'qish");
    expect([...n].sort()).toEqual(["idea:o'qish", "person:munger", "theme:bilim", "work:kitob"]);
  });

  it("only follows the given visible links", () => {
    const n = neighbourhood(g.links, "idea:o'qish", new Set([3]));
    expect([...n].sort()).toEqual(["idea:o'qish", "work:kitob"]);
  });

  it("an isolated node is its own neighbourhood", () => {
    expect([...neighbourhood([], "x")]).toEqual(["x"]);
  });
});
