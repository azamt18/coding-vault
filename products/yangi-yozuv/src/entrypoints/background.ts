import { DEFAULT_SITES, EXCLUDED_SITES } from '@/utils/sites';

const EXTRA_SITES_SCRIPT_ID = 'extra-sites';
const CONTENT_SCRIPT_FILE = '/content-scripts/content.js';

export default defineBackground(() => {
  // When the user switches the extension on for a new site from the popup,
  // start working there right away and on every later visit.
  browser.permissions.onAdded.addListener(async ({ origins = [] }) => {
    await syncExtraSites();
    for (const origin of origins) {
      const tabs = await browser.tabs.query({ url: origin });
      for (const tab of tabs) {
        if (tab.id === undefined) continue;
        await browser.scripting
          .executeScript({ target: { tabId: tab.id, allFrames: true }, files: [CONTENT_SCRIPT_FILE] })
          .catch(() => {}); // e.g. the tab is a browser page we can't touch
      }
    }
  });
  browser.permissions.onRemoved.addListener(syncExtraSites);
  browser.runtime.onInstalled.addListener(syncExtraSites);
});

/** Registers the content script for every site the user added beyond the defaults. */
async function syncExtraSites() {
  const { origins = [] } = await browser.permissions.getAll();
  const extra = origins.filter((origin) => !DEFAULT_SITES.includes(origin));

  const existing = await browser.scripting.getRegisteredContentScripts({
    ids: [EXTRA_SITES_SCRIPT_ID],
  });
  if (existing.length) {
    await browser.scripting.unregisterContentScripts({ ids: [EXTRA_SITES_SCRIPT_ID] });
  }
  if (!extra.length) return;

  await browser.scripting.registerContentScripts([
    {
      id: EXTRA_SITES_SCRIPT_ID,
      matches: extra,
      excludeMatches: EXCLUDED_SITES,
      js: [CONTENT_SCRIPT_FILE],
      allFrames: true,
      runAt: 'document_idle',
    },
  ]);
}
