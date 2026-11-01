# Chrome Web Store listing

Copy these into the Developer Dashboard. The Uzbek text uses the *current*
spelling (oʻ, sh, ch), because that's what people type when they search the store.

## Store listing tab

**Name** (from the manifest): Yangi Yozuv: Ş Ç Ö Ğ

**Summary** (from the manifest, ≤132 chars):
Yangi özbek alifbosida yozing: sh→ş, ch→ç, oʻ→ö, gʻ→ğ avtomatik. Type the new Uzbek alphabet as you write.

**Category:** Tools
**Language:** English (Uzbek isn't offered as a store language; the description below is bilingual)

**Description:**

```
Yangi oʻzbek alifbosida odatdagidek yozing.

2027-yil 22-apreldan yangi lotin alifbosi kuchga kiradi: Sh → Ş, Ch → Ç, Oʻ → Ö, Gʻ → Ğ. Yangi harflarni klaviaturadan qidirish shart emas. Odatdagidek yozavering, Yangi Yozuv soʻzni avtomatik almashtiradi:

  shahar → şahar
  choy → çoy
  oʻzbek → özbek
  togʻ → toğ

• Inglizcha soʻzlar, havolalar, email va @username oʻzgarmaydi.
• Xato almashtirsa, darhol Backspace bosing: soʻz qaytadi.
• Ismlar va brendlar uchun "oʻzgartirilmaydigan soʻzlar" roʻyxati.
• Telegram Web, Gmail, Facebook, Instagram, WhatsApp Web va barcha .uz saytlarda ishlaydi. Boshqa saytda bir tugma bilan yoqiladi.

Hech narsa kompyuteringizdan chiqmaydi. Yozganlaringiz hech qayerga yuborilmaydi: kengaytma internetga umuman murojaat qilmaydi.

—

Type the new Uzbek Latin alphabet the way you already type.

From 22 April 2027, Uzbek replaces Sh, Ch, Oʻ and Gʻ with Ş, Ç, Ö and Ğ. Keep typing as usual and Yangi Yozuv converts each word when you finish it. English words, links, emails and @usernames are left alone, and one Backspace undoes a conversion.

Everything runs inside your browser. Nothing you type is ever sent anywhere: the extension makes no network requests at all.
```

**Graphics:**
- Icon: `public/icon/128.png`
- Screenshot: `store/screenshot-1280x800.png`
- Small promo tile: `store/promo-440x280.png`

## Privacy practices tab

**Single purpose:**
Converts Uzbek words typed in the old Latin spelling (sh, ch, oʻ, gʻ) to the new 2027 alphabet (ş, ç, ö, ğ) as the user types.

**Permission justifications:**
- `storage`: saves the user's settings (on/off, sites turned off, words never to convert) in the browser.
- `scripting`: starts the extension on sites the user turns on from the popup.
- `activeTab`: reads the current tab's address when the popup opens, to show whether the extension works on that site.
- Host permissions (content script on listed sites, optional on others): the extension needs to see what the user types in text fields on those sites to convert it. The text is processed locally and never leaves the device.
- Remote code: **No**, all code is bundled.

**Data usage:** tick nothing. The extension does not collect or transmit any user data.
Certify all three statements (no selling, no unrelated use, no creditworthiness use).

**Privacy policy URL:** host `PRIVACY.md` (e.g. a public GitHub repo or Gist) and paste the link.
