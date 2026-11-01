// Opens the built popup in Chrome for Testing and saves screenshots (light and dark).
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const extensionPath = fileURLToPath(new URL('../.output/chrome-mv3', import.meta.url));
const outDir = fileURLToPath(new URL('../store/', import.meta.url));

const browser = await puppeteer.launch({ headless: true, pipe: true, enableExtensions: [extensionPath] });
try {
  const worker = await browser.waitForTarget((t) => t.type() === 'service_worker');
  const extensionId = new URL(worker.url()).host;
  const page = await browser.newPage();
  await page.setViewport({ width: 300, height: 520, deviceScaleFactor: 2 });
  await page.goto(`chrome-extension://${extensionId}/popup.html`);
  await page.type('#skip-input', 'Shohruh');
  await page.click('#skip-form button');
  await new Promise((r) => setTimeout(r, 300));
  for (const scheme of ['light', 'dark']) {
    await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: scheme }]);
    const body = await page.$('body');
    await body.screenshot({ path: `${outDir}popup-${scheme}.png` });
  }
  console.log('saved popup-light.png and popup-dark.png');
} finally {
  await browser.close();
}
