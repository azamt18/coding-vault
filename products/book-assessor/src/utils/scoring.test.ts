import { describe, expect, it } from "vitest";
import type { QuestionBank } from "../types";
import { getRecommendation, scoreAssessment } from "./scoring";

describe("getRecommendation", () => {
  it("skips at exactly 0.8", () => {
    expect(getRecommendation(2, 0.8)).toBe("skip");
  });
  it("skims just below 0.8", () => {
    expect(getRecommendation(2, 0.79)).toBe("skim");
  });
  it("skims at exactly 0.5", () => {
    expect(getRecommendation(2, 0.5)).toBe("skim");
  });
  it("reads just below 0.5", () => {
    expect(getRecommendation(2, 0.49)).toBe("read");
  });
  it("always skims the intro and chapter 1", () => {
    for (const chapter of [0, 1]) {
      expect(getRecommendation(chapter, 0.95)).toBe("skim");
      expect(getRecommendation(chapter, 0)).toBe("skim");
    }
  });
});

describe("scoreAssessment", () => {
  const mk = (id: string, chapter: number, correctAnswer: string) => ({
    id,
    chapter,
    type: "recall" as const,
    prompt: "p",
    options: ["a", "b", "c", "d"],
    correctAnswer,
  });
  const bank: QuestionBank = {
    0: [mk("a1", 0, "A"), mk("a2", 0, "B")],
    2: [mk("b1", 2, "A"), mk("b2", 2, "B")],
    3: [mk("c1", 3, "A"), mk("c2", 3, "B")],
  };

  it("scores per chapter, in order, with recommendations", () => {
    const scores = scoreAssessment(bank, {
      a1: "A",
      a2: "B", // chapter 0: 100%, still skim (foundational)
      b1: "A",
      b2: "B", // chapter 2: 100%, skip
      c1: "A",
      c2: "C", // chapter 3: 50%, skim
    });
    expect(scores).toEqual([
      { chapter: 0, score: 1, recommendation: "skim" },
      { chapter: 2, score: 1, recommendation: "skip" },
      { chapter: 3, score: 0.5, recommendation: "skim" },
    ]);
  });

  it("counts unanswered questions as incorrect", () => {
    const scores = scoreAssessment(bank, { b1: "A" });
    expect(scores.find((s) => s.chapter === 2)).toEqual({
      chapter: 2,
      score: 0.5,
      recommendation: "skim",
    });
    expect(scores.find((s) => s.chapter === 3)?.recommendation).toBe("read");
  });
});
