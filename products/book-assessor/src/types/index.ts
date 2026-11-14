/**
 * Core type definitions for the book assessment application.
 */

/**
 * Question type: recall (fact retrieval), application (concept use), or critical (analysis/synthesis).
 */
export type QuestionType = "recall" | "application" | "critical";

/**
 * Reading recommendation based on chapter score.
 */
export type Recommendation = "skip" | "skim" | "read";

/**
 * Represents a chapter in a book.
 */
export interface Chapter {
  number: number;
  title: string;
  isFoundational: boolean;
}

/**
 * Represents a book with its metadata and chapters.
 */
export interface Book {
  title: string;
  author: string;
  chapters: Chapter[];
}

/**
 * Represents a single assessment question.
 */
export interface Question {
  id: string;
  chapter: number;
  type: QuestionType;
  prompt: string;
  options: string[];
  correctAnswer: string;
}

/**
 * Maps chapter numbers to their questions.
 */
export type QuestionBank = Record<number, Question[]>;

/**
 * Represents the score for a single chapter.
 */
export interface ChapterScore {
  chapter: number;
  score: number; // 0–1
  recommendation: Recommendation;
}

/**
 * Represents the complete assessment results for a book.
 */
export interface AssessmentResult {
  book: Book;
  scores: ChapterScore[];
  answers: Record<string, string>;
}
