// Builds src/core/data/english-words.json: common English words that the
// converter must leave alone. Only words containing "sh" or "ch" matter, so
// the bundle stays small. Source: SCOWL via wordlist-english (MIT).
import { writeFileSync } from 'node:fs';
import wordlist from 'wordlist-english';

const TIERS = ['10', '20', '35', '40'];
const DIALECTS = ['english', 'english/american', 'english/british'];

const words = new Set();
for (const dialect of DIALECTS) {
  for (const tier of TIERS) {
    for (const word of wordlist[`${dialect}/${tier}`]) {
      const lower = word.toLowerCase();
      if (/sh|ch/.test(lower)) words.add(lower);
    }
  }
}

// English words that need an apostrophe after o/g and so would otherwise turn into ö/ğ.
for (const extra of ["o'clock", "o'er"]) words.add(extra);

const sorted = [...words].sort();
writeFileSync(
  new URL('../src/core/data/english-words.json', import.meta.url),
  JSON.stringify(sorted) + '\n',
);
console.log(`english-words.json: ${sorted.length} words`);
