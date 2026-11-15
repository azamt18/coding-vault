import type { Book, Chapter } from "../types";
import { DEFAULT_BOOK_TITLE, FOUNDATIONAL_CHAPTERS } from "./constants";

const SEARCH_URL = "https://openlibrary.org/search.json";

// chapter titles are hardcoded: open library does not expose a table of contents reliably.
// source: the official companion site, anxiousgeneration.com/research/supplements-for-each-chapter
// (chapters 1-13); the introduction title comes from search-result snippets only.
export const ANXIOUS_GENERATION_TITLES: readonly string[] = [
  "Introduction: Growing Up on Mars",
  "The Surge of Suffering",
  "What Children Need to Do in Childhood",
  "Discover Mode and the Need for Risky Play",
  "Puberty and the Blocked Transition to Adulthood",
  "The Four Basic Harms",
  "Why Social Media Harms Girls More Than Boys",
  "What Is Happening to Boys?",
  "Spiritual Degradation and Elevation",
  "Preparing for Collective Action",
  "What Governments and Tech Companies Can Do Now",
  "What Schools Can Do Now",
  "What Parents Can Do Now",
  "Bring Childhood Back to Earth",
];

export function buildChapters(titles: readonly string[]): Chapter[] {
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

export const FETCH_TIMEOUT_MS = 8000;
export const OFFLINE_NOTE = "offline: using built-in book data";

const AUTHOR_NAME = "Jonathan Haidt";

/** the built-in book, used when open library is unreachable or returns something unexpected. */
export function localBook(): Book {
  return {
    title: DEFAULT_BOOK_TITLE,
    author: AUTHOR_NAME,
    chapters: buildChapters(ANXIOUS_GENERATION_TITLES),
  };
}

function assertSupported(title: string): void {
  if (title.trim().toLowerCase() !== DEFAULT_BOOK_TITLE.toLowerCase()) {
    throw new Error(`no chapter data available for "${title}"`);
  }
}

/**
 * fetches book metadata from open library and attaches hardcoded chapters.
 * only "the anxious generation" has chapter data; other titles throw.
 * throws if no result has an author containing "haidt".
 */
export async function fetchBookByTitle(
  title: string,
  fetchFn: typeof fetch = fetch,
  signal?: AbortSignal,
): Promise<Book> {
  assertSupported(title);

  const url = `${SEARCH_URL}?title=${encodeURIComponent(title)}&author=haidt&limit=5`;
  const res = await fetchFn(url, { signal });
  if (!res.ok) {
    throw new Error(`open library request failed: ${res.status}`);
  }
  const data = (await res.json()) as { docs?: SearchDoc[] };
  const author = data.docs
    ?.flatMap((d) => d.author_name ?? [])
    .find((a) => a.toLowerCase().includes("haidt"));
  const doc = data.docs?.find((d) =>
    d.author_name?.some((a) => a.toLowerCase().includes("haidt")),
  );
  if (!doc || !author) {
    throw new Error(`book not found on open library: "${title}"`);
  }

  return {
    title: doc.title ?? DEFAULT_BOOK_TITLE,
    author,
    chapters: buildChapters(ANXIOUS_GENERATION_TITLES),
  };
}

export interface LoadedBook {
  book: Book;
  offline: boolean;
}

/**
 * like fetchBookByTitle, but never dead-ends: on error, timeout or a non-haidt
 * result it falls back to the built-in book. unsupported titles still throw.
 */
export async function loadBook(
  title: string,
  fetchFn: typeof fetch = fetch,
  timeoutMs: number = FETCH_TIMEOUT_MS,
  outerSignal?: AbortSignal,
): Promise<LoadedBook> {
  assertSupported(title);
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  outerSignal?.addEventListener("abort", () => controller.abort());
  try {
    const book = await fetchBookByTitle(title, fetchFn, controller.signal);
    return { book, offline: false };
  } catch {
    return { book: localBook(), offline: true };
  } finally {
    clearTimeout(timer);
  }
}
