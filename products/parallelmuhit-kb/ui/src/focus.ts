import type { KbLink } from "./data";

// the node and its direct neighbours, following links in both directions.
// pass visibleLinks to follow only links the filters currently show.
export function neighbourhood(links: KbLink[], id: string, visibleLinks?: Set<number>): Set<string> {
  const out = new Set([id]);
  links.forEach((l, i) => {
    if (visibleLinks && !visibleLinks.has(i)) return;
    if (l.source === id) out.add(l.target);
    else if (l.target === id) out.add(l.source);
  });
  return out;
}
