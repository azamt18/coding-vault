/**
 * Sites where the extension works right after install. Any other site needs
 * the user to switch it on from the popup, which asks for that one site only.
 * Keeping this list short keeps the install warning short.
 */
export const DEFAULT_SITES = [
  '*://*.uz/*', // kun.uz, olx.uz, my.gov.uz, hh.uz and every other .uz site
  '*://web.telegram.org/*',
  '*://mail.google.com/*',
  '*://web.whatsapp.com/*',
  '*://*.facebook.com/*',
  '*://*.instagram.com/*',
  '*://*.x.com/*',
  '*://*.linkedin.com/*',
  '*://*.youtube.com/*',
  '*://outlook.live.com/*',
  '*://outlook.office.com/*',
  '*://chatgpt.com/*',
  '*://gemini.google.com/*',
  '*://claude.ai/*',
];

// Google Docs draws its own text instead of using editable page text, so
// typing there can't be converted yet.
export const EXCLUDED_SITES = ['*://docs.google.com/*'];

/** The match pattern that covers exactly one hostname. */
export function siteOrigin(hostname: string): string {
  return `*://${hostname}/*`;
}
