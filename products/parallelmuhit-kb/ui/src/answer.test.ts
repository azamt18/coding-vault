import { describe, expect, it } from "vitest";
import { answerView, essayNodeId, type AskResult } from "./answer";

const base: AskResult = {
  question: "Taleb?",
  answer: "Taleb yozadi [001_a#p1, 002_b#p3]. Boshqa gap.",
  dropped: [],
  flagged: false,
  citations: [
    { id: "001_a#p1", title: "A", url: "https://parallelmuhit.uz/a", quote: "q1", links: [{ text: "x", url: "https://u.example" }] },
    { id: "002_b#p3", title: "B", url: "javascript:alert(1)", quote: "q2", links: [{ text: "bad", url: "javascript:x" }] },
  ],
};

describe("essayNodeId", () => {
  it("maps a paragraph id to its essay node", () => {
    expect(essayNodeId("003_javoblar#p13")).toBe("essay:003_javoblar");
  });
});

describe("answerView", () => {
  it("splits the answer into text and citation segments, one per id", () => {
    const v = answerView(base);
    expect(v.segments).toEqual([
      { text: "Taleb yozadi " },
      { cite: "001_a#p1" }, { text: " " }, { cite: "002_b#p3" },
      { text: ". Boshqa gap." },
    ]);
  });

  it("only links http(s) urls, for the essay and for the paragraph links", () => {
    const [a, b] = answerView(base).citations;
    expect(a.essayUrl).toBe("https://parallelmuhit.uz/a");
    expect(a.links.map((l) => l.href)).toEqual(["https://u.example"]);
    expect(b.essayUrl).toBeNull();
    expect(b.links).toEqual([]);
  });

  it("shows a warning naming the dropped ids when a citation was dropped", () => {
    const v = answerView({ ...base, dropped: ["999_x#p1"], flagged: true });
    expect(v.warning).toContain("999_x#p1");
  });

  it("warns without ids when flagged only for having no checked source", () => {
    const v = answerView({ ...base, citations: [], answer: "gap", flagged: true });
    expect(v.warning).toBeTruthy();
    expect(v.warning).not.toContain("undefined");
  });

  it("has no warning for a clean answer and no citation segments for plain text", () => {
    expect(answerView(base).warning).toBeNull();
    expect(answerView({ ...base, answer: "essalarda bu haqda topilmadi", citations: [] }).segments)
      .toEqual([{ text: "essalarda bu haqda topilmadi" }]);
  });

  it("does not make a link of an id that has no checked citation", () => {
    const v = answerView({ ...base, answer: "gap [777_z#p1]." });
    expect(v.segments).toEqual([{ text: "gap [777_z#p1]." }]);
  });
});
