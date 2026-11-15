/**
 * Global constants for the book assessment application.
 */

/**
 * Score threshold: score ≥0.8 → skip chapter.
 */
export const SKIP_THRESHOLD = 0.8;

/**
 * Score threshold: score ≥0.5 (and <0.8) → skim chapter; score <0.5 → read chapter.
 */
export const SKIM_THRESHOLD = 0.5;

/**
 * Chapters that should always be recommended for skimming (foundational chapters).
 */
export const FOUNDATIONAL_CHAPTERS: readonly number[] = [0, 1];

/**
 * Default book title used in the application.
 */
export const DEFAULT_BOOK_TITLE = "The Anxious Generation";
