import { useEffect, useState } from "react";
import type { Book } from "../types";
import { loadBook } from "../utils/openLibrary";

/**
 * fetches book metadata whenever the title changes.
 * ignores stale responses so a slow earlier request can't overwrite a newer one.
 */
export function useOpenLibrary(title: string) {
  const [book, setBook] = useState<Book | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [offline, setOffline] = useState(false);

  useEffect(() => {
    if (!title.trim()) {
      setBook(null);
      setLoading(false);
      setError(null);
      setOffline(false);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError(null);
    setOffline(false);

    const controller = new AbortController();
    loadBook(title, undefined, undefined, controller.signal)
      .then(({ book: b, offline: o }) => {
        if (cancelled) return;
        setBook(b);
        setOffline(o);
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
      controller.abort();
    };
  }, [title]);

  return { book, loading, error, offline };
}
