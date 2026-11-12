// render model for the question box; pure so it tests without a DOM. The server already dropped fake ids,
// so every quote and url here comes from the data, never from model text.
import { urlItems, type KbUrl, type UrlItem } from "./urls";

export interface Citation {
  id: string;
  title: string;
  url: string;
  quote: string;
  links: KbUrl[];
}

export interface AskResult {
  question: string;
  answer: string;
  dropped: string[];
  flagged: boolean;
  citations: Citation[];
}

export type Segment = { text: string } | { cite: string };

export interface CitationView {
  id: string;
  title: string;
  quote: string;
  essayUrl: string | null;
  links: UrlItem[];
}

export interface AnswerView {
  segments: Segment[];
  citations: CitationView[];
  warning: string | null;
}

export const essayNodeId = (paragraphId: string): string => `essay:${paragraphId.split("#")[0]}`;

const BRACKET = /\[([^\[\]]*#p\d+[^\[\]]*)\]/g;
const ID = /[\w]+#p\d+/g;

export function answerView(r: AskResult): AnswerView {
  const checked = new Set(r.citations.map((c) => c.id));
  const segments: Segment[] = [];
  let text = "";
  const flush = () => { if (text) segments.push({ text }); text = ""; };
  let last = 0;
  for (const m of r.answer.matchAll(BRACKET)) {
    const ids = (m[1].match(ID) ?? []).filter((i) => checked.has(i));
    if (!ids.length) continue; // not a checked citation: leave the text as the model wrote it
    text += r.answer.slice(last, m.index);
    flush();
    ids.forEach((id, k) => { if (k) segments.push({ text: " " }); segments.push({ cite: id }); });
    last = m.index! + m[0].length;
  }
  text += r.answer.slice(last);
  flush();

  const citations = r.citations.map((c) => ({
    id: c.id,
    title: c.title,
    quote: c.quote,
    essayUrl: urlItems([{ text: c.title, url: c.url }])[0]?.href ?? null,
    links: urlItems(c.links),
  }));

  let warning: string | null = null;
  if (r.dropped.length) warning = `unchecked sources were removed: ${r.dropped.join(", ")}. do not trust this answer.`;
  else if (r.flagged) warning = "no checked source backs this answer. do not trust it.";
  return { segments, citations, warning };
}
