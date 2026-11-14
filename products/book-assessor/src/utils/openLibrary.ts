import type { Book, Chapter } from "../types";
import { DEFAULT_BOOK_TITLE, FOUNDATIONAL_CHAPTERS } from "./constants";

const SEARCH_URL = "https://openlibrary.org/search.json";

// chapter titles are hardcoded: open library does not expose a table of contents reliably.
const ANXIOUS_GENERATION_TITLES: readonly string[] = [
  "Introduction: The Great Rewiring",
  "A Surge of Suffering",
  "The Backstory: Overprotection in the Real World",
  "The Rise of the Phone-Based Childhood",
  "What Children Need to Do",
  "Four Foundational Harms",
  "Why Social Media Harms Girls More Than Boys",
  "Why the Phone-Based Childhood Harms Boys",
  "Spiritual Elevation and Degradation",
  "Collective Action for Teens",
  "What Governments and Tech Companies Can Do",
  "What Schools Can Do",
  "What Parents Can Do",
];

function buildChapters(titles: readonly string[]): Chapter[] {
  return titles.map((title, number) => ({
    number,
    title,
    isFoundational: FOUNDATIONAL_CHAPTERS.includes(number),
  }));
}

interface SearchDoc {
  title?: string;
  author_name?: string[];
}

/**
 * fetches book metadata from open library and attaches hardcoded chapters.
 * only "the anxious generation" has chapter data; other titles throw.
 */
export async function fetchBookByTitle(
  title: string,
  fetchFn: typeof fetch = fetch,
): Promise<Book> {
  const normalized = title.trim().toLowerCase();
  if (normalized !== DEFAULT_BOOK_TITLE.toLowerCase()) {
    throw new Error(`no chapter data available for "${title}"`);
  }

  const url = `${SEARCH_URL}?title=${encodeURIComponent(title)}&limit=1`;
  const res = await fetchFn(url);
  if (!res.ok) {
    throw new Error(`open library request failed: ${res.status}`);
  }
  const data = (await res.json()) as { docs?: SearchDoc[] };
  const doc = data.docs?.[0];
  if (!doc) {
    throw new Error(`book not found on open library: "${title}"`);
  }

  return {
    title: doc.title ?? DEFAULT_BOOK_TITLE,
    author: doc.author_name?.[0] ?? "Unknown",
    chapters: buildChapters(ANXIOUS_GENERATION_TITLES),
  };
}
