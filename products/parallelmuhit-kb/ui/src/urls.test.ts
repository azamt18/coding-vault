import { describe, expect, it } from "vitest";
import { urlItems } from "./urls";

describe("urlItems", () => {
  it("renders every url as a new-tab link with an arrow and the anchor text", () => {
    expect(urlItems([{ text: "qarang", url: "https://youtu.be/abc" }])).toEqual([
      { href: "https://youtu.be/abc", label: "↗ qarang", target: "_blank", rel: "noopener noreferrer" },
    ]);
  });

  it("renders nothing when urls are absent or empty", () => {
    expect(urlItems(undefined)).toEqual([]);
    expect(urlItems([])).toEqual([]);
  });

  it("never renders a non-http url", () => {
    expect(urlItems([{ text: "x", url: "javascript:alert(1)" }])).toEqual([]);
  });
});
