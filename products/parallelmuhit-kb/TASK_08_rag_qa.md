# task 08: rag q&a over the graph (draft, needs the user's ok)

written 2026-11-12 by the plan session. this is the original goal. starts after task 07, because answers should cite urls too.

## goal

the user asks a question in uzbek ("Aziz Rahimov Taleb haqida nima deydi?", "qaysi kitoblarni tavsiya qiladi?") and gets a short uzbek answer, every claim tied to an essay paragraph, with the quote and the essay's url.

## design (recommended defaults)

1. **retrieval, no embeddings, no api key.**
   - graph side: find entities named in the question (same normalisation as the ui search). take their links and quotes (1 hop).
   - text side: bm25 over all paragraphs (about 6k). uzbek is agglutinative, so cut every token to its first 5 letters (cheap stemmer), and drop short stop words. pure python, no new heavy dependency.
   - merge both lists, rank, cap at about 12 paragraphs + 20 link quotes (keeps the prompt small and the subscription cheap).
2. **generation.** `claude -p` with sonnet, same backend as tasks 03-05. the prompt: answer in uzbek, only from the given context, cite `[003_javoblar#p13]` after each claim, say "essalarda bu haqda topilmadi" when the context does not answer.
3. **verification by code.** every cited id must be in the context given; a citation that is not is dropped and the answer is flagged. the quotes shown to the user are copied from the paragraph text by code, never written by the model.
4. **interface.** step 1: cli `ask.py "savol"` prints the answer, then the cited quotes and urls. step 2 (later, separate task): a question box in the ui, which needs a tiny local python server because `claude -p` can't run in the browser.
5. **eval.** 12 questions: 6 written by the user (with the essay they expect), 6 by the plan. pass = the expected essay is cited, no cited id is fake, and "not found" is returned for 2 questions that the essays can't answer.

## open decisions for the user

- is bm25 + graph enough, or do you want embeddings too (needs an openrouter key and costs money)? recommendation: start without, measure on the eval, add only if it misses.
- cli first, ui box later: ok?
