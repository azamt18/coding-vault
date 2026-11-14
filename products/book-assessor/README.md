# kitoblab

checks how much of a book you already know and turns the result into a per-chapter reading plan: skip, skim or read.

## what it does

you answer a set of expert-written multiple-choice questions about the book. each chapter gets a score, and the score maps to a recommendation:

- 80% or more: skip
- 50-79%: skim
- under 50%: read
- the introduction and chapter 1 are foundational, so they are always skim, whatever the score.

## how to use

1. open the app.
2. wait for the book to load (metadata comes from open library).
3. answer all the questions upfront.
4. run the assessment.
5. download the markdown report.

## example output

```markdown
# the anxious generation - reading plan

| chapter | score | recommendation |
| --- | --- | --- |
| 0. introduction: the great rewiring | 100% | skim |
| 2. the backstory: overprotection in the real world | 67% | skim |
| 3. the rise of the phone-based childhood | 33% | read |
```

the real report also has an expandable section per chapter listing each question and your answer.

## how to add another book

1. add a question json next to `src/data/anxious-generation.json` (same shape: chapter number to a list of questions) and wire it up in `src/App.tsx`.
2. add the chapter titles in `src/utils/openLibrary.ts` and allow the new title in `fetchBookByTitle`, which currently only accepts "the anxious generation".

## development

```bash
npm install
npm run dev     # local dev server
npm test        # vitest, single run
npm run build   # type-check + production build into dist
```

## known caveats

- chapter titles and question themes were written from memory and must be verified against the real table of contents before launch.
- only "the anxious generation" is supported.
- there are no tests for the ui, only for the scoring logic.

## deploy to lovable

status: not yet done (human step).

- import the github repo, or the `products/book-assessor` folder, into lovable.
- build command: `npm run build`
- output directory: `dist`
