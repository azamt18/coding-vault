import { useEffect } from "react";
import type { Book } from "../types";
import { useOpenLibrary } from "../hooks";

interface BookLoaderProps {
  title?: string;
  // called once the book has loaded, so the parent can store it
  onLoaded?: (book: Book) => void;
}

/**
 * fetches the book and shows loading, error or loaded status.
 */
export function BookLoader({
  title = "The Anxious Generation",
  onLoaded,
}: BookLoaderProps) {
  const { book, loading, error } = useOpenLibrary(title);

  useEffect(() => {
    if (book && onLoaded) onLoaded(book);
  }, [book, onLoaded]);

  if (loading) return <p role="status">loading book...</p>;
  if (error) return <p role="alert">could not load book: {error}</p>;
  if (!book) return null;
  return <p>book loaded: {book.chapters.length} chapters</p>;
}
