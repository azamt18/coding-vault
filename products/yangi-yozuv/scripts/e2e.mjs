// Loads the built extension into Chrome for Testing and types into real text
// fields on a fake .uz page. Run `npm run build` first.
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const extensionPath = fileURLToPath(new URL('../.output/chrome-mv3', import.meta.url));

const PAGE = `<!doctype html><meta charset="utf-8">
<input id="input" type="text">
<textarea id="textarea"></textarea>
<div id="editor" contenteditable="true"></div>
<input id="email" type="email">
<div id="chat" contenteditable="true"></div>
<script>
  // Behaves like a chat app: Enter sends whatever is in the box.
  window.sent = [];
  chat.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter') return;
    e.preventDefault();
    window.sent.push(chat.textContent);
    chat.textContent = '';
  });
</script>`;

const browser = await puppeteer.launch({
  headless: true,
  pipe: true,
  enableExtensions: [extensionPath],
});

let failures = 0;
function check(name, actual, expected) {
  const ok = actual === expected;
  if (!ok) failures++;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${name}: ${JSON.stringify(actual)}${ok ? '' : ` (expected ${JSON.stringify(expected)})`}`);
}

try {
  const page = await browser.newPage();
  await page.setRequestInterception(true);
  page.on('request', (request) =>
    request.url().startsWith('https://test.uz/')
      ? request.respond({ contentType: 'text/html', body: PAGE })
      : request.continue(),
  );
  await page.goto('https://test.uz/');
  await new Promise((resolve) => setTimeout(resolve, 500)); // let the content script start

  // Editable areas use a non-breaking space at the end of the text.
  const valueOf = (selector) =>
    page.$eval(selector, (el) => ('value' in el ? el.value : el.textContent).replace(/\u00a0/g, ' '));

  await page.type('#input', "Men shahar choy shop oldim, o'zbek tog' ");
  check('input', await valueOf('#input'), 'Men şahar çoy shop oldim, özbek toğ ');

  await page.type('#textarea', 'Toshkent\nchiroyli. ');
  check('textarea', await valueOf('#textarea'), 'Toşkent\nçiroyli. ');

  await page.type('#editor', "Assalomu alaykum, ishlar qalay? Yaxshi ");
  check('contenteditable', await valueOf('#editor'), 'Assalomu alaykum, işlar qalay? Yaxşi ');

  await page.type('#input', 'shohruh ');
  await page.keyboard.press('Backspace');
  check('backspace undo', await valueOf('#input'), 'Men şahar çoy shop oldim, özbek toğ shohruh ');

  await page.keyboard.press('Backspace');
  check('second backspace deletes normally', await valueOf('#input'), 'Men şahar çoy shop oldim, özbek toğ shohruh');

  await page.type('#email', 'shahzod@mail.uz ');
  check('email field untouched', await valueOf('#email'), 'shahzod@mail.uz');

  const tail = 'https://shop.uz/chegirma shahar.uz shahzod@mail.uz @shahzod ';
  await page.type('#input', ` ${tail}`);
  check('links, domains, emails and handles untouched', (await valueOf('#input')).endsWith(` ${tail}`), true);

  await page.type('#input', 'Shahar. Choy: yaxshi ');
  check(
    'sentence-ending dot and colon still convert',
    (await valueOf('#input')).endsWith('Şahar. Çoy: yaxşi '),
    true,
  );

  await page.type('#chat', 'Rahmat, yaxshi');
  await page.keyboard.press('Enter');
  check('chat Enter converts before sending', await page.evaluate(() => window.sent[0]), 'Rahmat, yaxşi');
} finally {
  await browser.close();
}

console.log(failures ? `${failures} failed` : 'all passed');
process.exit(failures ? 1 : 0);
