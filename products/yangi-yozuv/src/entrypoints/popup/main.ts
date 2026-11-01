import { disabledSitesItem, enabledItem, skipWordsItem } from '@/utils/settings';
import { siteOrigin } from '@/utils/sites';

const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;

async function setUpEnabledSwitch() {
  const input = $<HTMLInputElement>('enabled');
  input.checked = await enabledItem.getValue();
  input.addEventListener('change', () => enabledItem.setValue(input.checked));
}

async function setUpSiteRow() {
  const [tab] = await browser.tabs.query({ active: true, currentWindow: true });
  const url = tab?.url ? new URL(tab.url) : null;
  if (!url || !url.protocol.startsWith('http')) {
    $('site-unsupported').hidden = false;
    return;
  }

  const hostname = url.hostname;
  $('site-name').textContent = hostname;
  const covered = await browser.permissions.contains({ origins: [siteOrigin(hostname)] });

  if (!covered) {
    const button = $<HTMLButtonElement>('site-grant');
    button.hidden = false;
    // The background worker starts the extension on this site once granted.
    button.addEventListener('click', () =>
      browser.permissions.request({ origins: [siteOrigin(hostname)] }).then((granted) => {
        if (granted) window.close();
      }),
    );
    return;
  }

  const input = $<HTMLInputElement>('site-enabled');
  $('site-toggle').hidden = false;
  input.checked = !(await disabledSitesItem.getValue()).includes(hostname);
  input.addEventListener('change', async () => {
    const others = (await disabledSitesItem.getValue()).filter((site) => site !== hostname);
    await disabledSitesItem.setValue(input.checked ? others : [...others, hostname]);
  });
}

async function setUpSkipWords() {
  const list = $<HTMLUListElement>('skip-list');
  const input = $<HTMLInputElement>('skip-input');

  const render = (words: string[]) => {
    list.replaceChildren(
      ...words.map((word) => {
        const item = document.createElement('li');
        const remove = document.createElement('button');
        remove.type = 'button';
        remove.textContent = '×';
        remove.ariaLabel = `Öçiriş: ${word}`;
        remove.addEventListener('click', async () => {
          const current = await skipWordsItem.getValue();
          await skipWordsItem.setValue(current.filter((w) => w !== word));
        });
        item.append(word, remove);
        return item;
      }),
    );
  };

  render(await skipWordsItem.getValue());
  skipWordsItem.watch(render);

  $<HTMLFormElement>('skip-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const word = input.value.trim().toLowerCase();
    input.value = '';
    if (!word) return;
    const current = await skipWordsItem.getValue();
    if (!current.includes(word)) await skipWordsItem.setValue([...current, word].sort());
  });
}

setUpEnabledSwitch();
setUpSiteRow();
setUpSkipWords();
