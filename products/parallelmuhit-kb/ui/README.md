# parallelmuhit graph explorer

a local static page over `../extract/graph_grouped.json`. vite + typescript, graphology + sigma 3, forceatlas2 in a web worker. no backend.

```sh
npm install
npm run dev      # copies the graph json into public/ (sync_data.sh), then serves it
npm test         # vitest: search, filters, neighbourhood, data loader smoke test
npm run build    # typecheck + static build into dist/
```

the data path is one constant, `DATA_URL` in `src/data.ts` (default `/graph_grouped.json`).

## what it does

- colour by node type and link kind, node size by `mention_count` (essays, themes, author by degree; capped).
- click a node: label, type, aliases, theme, per-essay descriptions, links grouped by kind with essay, paragraph and quote. click the other end to jump.
- filters: node types, link kinds, one essay. they combine (intersection). defaults hide essay nodes and `wrote` / `mentioned_in` links; switch them on in the lists.
- search over label and aliases, ignoring case and apostrophe forms (‘ ʻ ' ’ ` ʼ).
- selecting a node dims everything but it and its visible neighbours. "clear focus" or a click on empty space clears it.
- weak links are shown as they are: only a filter hides a link.

## manual check list

- [ ] `npm run dev` shows the graph with the default filters, no console errors.
- [ ] search "munger" gives one person node (Charli Manger); picking it centres it and the panel lists links with quotes.
- [ ] picking an essay shrinks the graph to that essay's links; unticking a type and a kind each shrink it further; the count line shows the intersection.
- [ ] with every type and kind ticked and no essay, the count is 1961 nodes, 5035 links.
- [ ] "clear focus" undims the graph and empties the panel.
