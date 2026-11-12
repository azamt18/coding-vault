import type { KbNode } from "./data";

// same apostrophe set as merge_names.py (_APOSTROPHES)
const APOSTROPHES = /[‘ʻ'’`ʼ]/g;

export function fold(s: string): string {
  return s.normalize("NFC").toLowerCase().replace(APOSTROPHES, "").replace(/\s+/g, " ").trim();
}

// rank: 0 exact label, 1 label prefix, 2 exact alias, 3 label substring, 4 alias substring
function rank(n: KbNode, q: string): number {
  const label = fold(n.label);
  const aliases = (n.aliases ?? []).map(fold);
  if (label === q) return 0;
  if (label.startsWith(q)) return 1;
  if (aliases.includes(q)) return 2;
  if (label.includes(q)) return 3;
  if (aliases.some((a) => a.includes(q))) return 4;
  return -1;
}

export function search(nodes: KbNode[], query: string, limit = 10): KbNode[] {
  const q = fold(query);
  if (!q) return [];
  return nodes
    .map((n) => ({ n, r: rank(n, q) }))
    .filter((x) => x.r >= 0)
    .sort((a, b) => a.r - b.r || (b.n.mention_count ?? 0) - (a.n.mention_count ?? 0) || a.n.label.localeCompare(b.n.label))
    .slice(0, limit)
    .map((x) => x.n);
}
