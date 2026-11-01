import { convertWord, type ConvertOptions } from './convert';

export interface Conversion {
  /** Index where the original word starts. */
  start: number;
  /** Index right after the original word (the caret). */
  end: number;
  original: string;
  replacement: string;
}

// Apostrophes and hyphens don't end a word: oʻ, gʻ and qo'l-qo'l are mid-word.
// Neither do "." and ":", which can be part of a domain or link (shahar.uz,
// https://). Those words convert at the next space or Enter instead, once the
// whole token is visible; "shahar." still becomes "şahar." then.
const BOUNDARY = /^[\s,!?;)\]}"»…]$/u;

/** Whether typing `char` finishes the word before it. */
export function isWordBoundary(char: string): boolean {
  return BOUNDARY.test(char);
}

/**
 * Works out how to convert the word that ends at `caret`, or returns null
 * when there is no word there or converting it changes nothing.
 */
export function planConversion(
  text: string,
  caret: number,
  options: ConvertOptions = {},
): Conversion | null {
  let start = caret;
  while (start > 0 && !/\s/u.test(text.charAt(start - 1))) start--;
  if (start === caret) return null;

  const original = text.slice(start, caret);
  const replacement = convertWord(original, options);
  if (replacement === original) return null;

  return { start, end: caret, original, replacement };
}
