import { useEffect, useState } from "react";
import type { Book } from "../types";
import { fetchBookByTitle } from "../utils/openLibrary";

/**
 * fetches book metadata whenever the title changes.
 * ignores stale responses so a slow earlier request can't overwrite a newer one.
 */
export function useOpenLibrary(title: string) {
  const [book, setBook] = useState<Book | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!title.trim()) {
      setBook(null);
      setLoading(false);
      setError(null);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError(null);

    fetchBookByTitle(title)
      .then((b) => {
        if (cancelled) return;
        setBook(b);
        setLoading(false);
      })
      .catch((e: unknown) => {
        if (cancelled) return;
        setBook(null);
        setError(e instanceof Error ? e.message : String(e));
        setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [title]);

  return { book, loading, error };
}
