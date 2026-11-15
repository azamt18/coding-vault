import type { ChapterScore, QuestionBank, Recommendation } from "../types";
import {
  FOUNDATIONAL_CHAPTERS,
  SKIM_THRESHOLD,
  SKIP_THRESHOLD,
} from "./constants";

/**
 * Maps a chapter score (0-1) to a reading recommendation.
 * Foundational chapters are always "skim".
 */
export function getRecommendation(
  chapter: number,
  score: number
): Recommendation {
  if (FOUNDATIONAL_CHAPTERS.includes(chapter)) return "skim";
  if (score >= SKIP_THRESHOLD) return "skip";
  if (score >= SKIM_THRESHOLD) return "skim";
  return "read";
}

/**
 * Scores every chapter in the bank. Answers are keyed by question id.
 * Unanswered questions count as incorrect.
 */
export function scoreAssessment(
  questions: QuestionBank,
  answers: Record<string, string>
): ChapterScore[] {
  return Object.keys(questions)
    .map(Number)
    .sort((a, b) => a - b)
    .map((chapter) => {
      const qs = questions[chapter] ?? [];
      const correct = qs.filter((q) => answers[q.id] === q.correctAnswer).length;
      const score = qs.length === 0 ? 0 : correct / qs.length;
      return { chapter, score, recommendation: getRecommendation(chapter, score) };
    });
}
