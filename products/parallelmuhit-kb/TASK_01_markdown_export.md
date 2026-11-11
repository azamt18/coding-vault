# Задача 01: выгрузить эссе из API в Markdown

Цель: получить чистый корпус эссе в Markdown. Это единственный источник текста для будущего knowledge graph. PDF в `essays/` больше не используем.

## Что сделать

Новый скрипт `export_markdown.py` рядом с `download_essays.py`. Логику работы с API взять оттуда, Playwright и PDF не нужны.

1. **Список эссе:** `GET {API_BASE}/blog` с теми же заголовками, что в `download_essays.py` (`Authorization: Bearer`, `token`, `Origin`, `Referer`). Нумерация `site_number` — ровно как там: сортировка по `createdAt`, `enumerate(..., start=1)`, затем `i + 1`. Номера должны совпасть с именами PDF (`002_daraxt` и т. д.).
2. **Текст эссе:** `GET {API_BASE}/blog/slug/{slug}` → поле `content` (HTML).
3. **Сырой ответ:** сохранить JSON ответа как есть в `essays_raw/NNN_slug.json`, чтобы больше не ходить в API.
4. **Конвертация в Markdown:** `markdownify` (или `html2text`, если не пойдёт), ATX-заголовки.
   - Абзацы разделены одной пустой строкой, без жёстких переносов внутри абзаца.
   - Цитаты → `>`, ссылки и картинки → обычный Markdown-синтаксис (картинки оставить ссылками, не скачивать).
   - Никаких HTML-тегов в результате.
   - **Не трогать узбекские апострофы и символы** (`oʻ`, `gʻ`, `‘`, `'`): никакой нормализации на этом шаге.
5. **Сохранить** в `essays_md/NNN_slug.md` с frontmatter:
   ```
   ---
   number: 2
   slug: daraxt
   title: "Daraxtlardan rivojlanishni o'rganamiz"
   author: Alijanov Ibrohim
   created_at: <createdAt из API>
   source: https://parallelmuhit.uz/blog/<slug>   # проверить реальный формат URL
   ---
   ```
   Затем `# <title>` и текст.

## Параметры запуска

- Токен только из `--token` или переменной `TOKEN`, никогда не записывать в файлы и логи.
- `--number N`, `--range A-B` — как в `download_essays.py`.
- Существующие файлы пропускать, `--force` для перезаписи.
- Если есть `essays_raw/NNN_slug.json`, конвертировать из него без запроса к API (`--offline`).

## Проверка (обязательно перед тем, как считать задачу сделанной)

- Число `.md` файлов = числу эссе из API (сейчас PDF 51).
- `grep -l "<[a-z]" essays_md/*.md` ничего не находит.
- Открыть 3 файла глазами: `002_daraxt`, `149_qiziquvchanlik`, `180_mimetik`. Абзацы на месте, апострофы и узбекские буквы целы, цитаты оформлены.
- Короткий отчёт: сколько эссе, сколько слов всего, самое длинное и самое короткое.

## уточнения после проверки (plan, 2026-11-11)

- **число эссе:** 51 pdf — это только часть (002–010 и 140–181). нумерация идёт до 181, значит в api около 180 эссе. проверка: число `.md` = длине ответа `/blog`, а не 51. плюс: для каждого `essays/NNN_slug.pdf` есть `essays_md/NNN_slug.md` с тем же именем (так проверяем, что номера совпали).
- **frontmatter:** в заголовках бывают `'`, `"`, `:`. строки писать через `yaml.safe_dump(..., allow_unicode=True)` или `json.dumps(..., ensure_ascii=False)`, не через f-string.
- **сырые ответы:** кроме `essays_raw/NNN_slug.json` (ответ `/blog/slug/{slug}` как есть) сохранить ответ списка в `essays_raw/_list.json`. `--offline` берёт номера и метаданные из него и работает без токена.
- **относительные ссылки:** если `src`/`href` начинается с `/`, дописать домен (`API_BASE` для картинок, `https://parallelmuhit.uz` для страниц). картинки не скачивать.
- **git:** добавить `pdp/parallelmuhit/essays_md/` и `pdp/parallelmuhit/essays_raw/` в корневой `.gitignore`, как pdf (контент платный). коммитить только скрипт и `.gitignore`.
- **зависимости:** `markdownify` не установлен, `pip3 install markdownify`.
- **не трогать:** `chatterbox-finetuning` (сабмодуль, уже изменён), `download_essays.py`, `.claude/`.

## Вне рамок этой задачи

Извлечение сущностей, граф, интерфейс. Это следующие задачи.
