import englishWords from './data/english-words.json';
import { isProtectedToken } from './protected';

export interface ConvertOptions {
  /** Lowercase words the user never wants converted (names, brands). */
  skipWords?: ReadonlySet<string>;
}

// Apostrophes people type for the old oʻ/gʻ mark. U+02BC (ʼ) is the tutuq
// sign, a separate letter that stays in the new alphabet, so it's not here.
const MARKS = "'ʻ‘’`";

const OLD_LETTERS = new RegExp(`([sc])h|([og])[${MARKS}]`, 'giu');
const NEW_LETTERS: Record<string, string> = { s: 'ş', c: 'ç', o: 'ö', g: 'ğ' };

const ENGLISH = new Set<string>(englishWords);
// Words SCOWL lists as English that are everyday Uzbek words too.
const UZBEK_OVERRIDES = new Set(['chin', 'chop', 'tush', 'mash', 'chap']);

const IRISH_NAME = new RegExp(`^O[${MARKS}]\\p{Lu}\\p{Ll}`, 'u');
const LETTER = /\p{L}/u;

/** Converts one whitespace-free token, keeping punctuation around it. */
export function convertWord(token: string, options: ConvertOptions = {}): string {
  if (isProtectedToken(token)) return token;

  const { lead, core, trail } = splitPunctuation(token);
  if (!core) return token;

  const lower = core.toLowerCase();
  if (options.skipWords?.has(lower)) return token;
  if (ENGLISH.has(lower) && !UZBEK_OVERRIDES.has(lower)) return token;
  if (IRISH_NAME.test(core)) return token;

  return lead + convertLetters(core) + trail;
}

/** Converts every word in a block of text, keeping all whitespace as is. */
export function convertText(text: string, options: ConvertOptions = {}): string {
  return text.replace(/\S+/g, (token) => convertWord(token, options));
}

function convertLetters(word: string): string {
  return word.replace(OLD_LETTERS, (_match: string, sc: string | undefined, og: string | undefined) => {
    const first = (sc ?? og)!;
    const replacement = NEW_LETTERS[first.toLowerCase()]!;
    return first === first.toUpperCase() ? replacement.toUpperCase() : replacement;
  });
}

function splitPunctuation(token: string): { lead: string; core: string; trail: string } {
  const isMark = (i: number) => MARKS.includes(token.charAt(i));
  // A mark right after o/g belongs to the word: tog' → toğ.
  const isWordEnd = (i: number) =>
    LETTER.test(token.charAt(i)) || (isMark(i) && /[og]/i.test(token.charAt(i - 1)));

  let start = 0;
  while (start < token.length && !LETTER.test(token.charAt(start))) start++;
  let end = token.length;
  while (end > start && !isWordEnd(end - 1)) end--;

  // An opening quote means the closing one is a quote too: 'dog' stays 'dog'.
  if (start > 0 && isMark(start - 1) && end > start && isMark(end - 1)) end--;

  return {
    lead: token.slice(0, start),
    core: token.slice(start, end),
    trail: token.slice(end),
  };
}
