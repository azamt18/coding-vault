// Each rule protects one kind of token. When unsure, protect: a missed
// conversion is a small annoyance, a broken link or email is not.

const URL_SCHEME = /^[a-z][a-z\d+.-]*:\/\//i;
const WWW = /^www\./i;
// Letters on both sides of a dot: kitob.shop, shahar.uz, a.b. A dot at the
// end of a word ("shahar.") or before a space doesn't match.
const DOMAIN_OR_FILE = /[\p{L}\d]\.[\p{L}\d]/u;
// A lowercase letter followed by a capital inside one word: iPhone, ChatGPT,
// YouTube. Plain Uzbek words never have this, and Shahar / SHAHAR don't match.
const CAMEL_CASE = /\p{Ll}\p{Lu}/u;

/**
 * Tokens that are never converted, whatever letters they contain: links,
 * emails, @usernames, #hashtags, domain or file names, and brand names written
 * in camelCase (ChatGPT, iPhone). `token` is a whole whitespace-free chunk,
 * punctuation included, e.g. "(https://shop.uz)," or "@shahzod_dev".
 */
export function isProtectedToken(token: string): boolean {
  // Strip opening brackets and quotes so "(@shahzod)" is still seen as a handle.
  const body = token.replace(/^[("'“‘«[{]+/u, '');

  return (
    URL_SCHEME.test(body) ||
    WWW.test(body) ||
    body.startsWith('@') ||
    body.startsWith('#') ||
    body.includes('@') ||
    DOMAIN_OR_FILE.test(body) ||
    CAMEL_CASE.test(body)
  );
}
