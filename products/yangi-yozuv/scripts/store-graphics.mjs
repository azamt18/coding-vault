// Renders store/graphics.html into the Chrome Web Store screenshot (1280×800)
// and small promo tile (440×280). Run screenshot-popup.mjs first.
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const storeDir = fileURLToPath(new URL('../store/', import.meta.url));
const browser = await puppeteer.launch({ headless: true });
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 1200 });
  await page.goto(`file://${storeDir}graphics.html`, { waitUntil: 'load' });
  await (await page.$('#shot')).screenshot({ path: `${storeDir}screenshot-1280x800.png` });
  await (await page.$('#tile')).screenshot({ path: `${storeDir}promo-440x280.png` });
  console.log('saved screenshot-1280x800.png and promo-440x280.png');
} finally {
  await browser.close();
}
