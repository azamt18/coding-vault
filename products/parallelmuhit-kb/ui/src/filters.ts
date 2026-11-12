import { LINK_KINDS, NODE_TYPES, type KbGraph } from "./data";

export interface Filters {
  types: Set<string>;
  kinds: Set<string>;
  essay: string | null; // essay id without the "essay:" prefix, e.g. "002_daraxt"
}

// essays and the essay-structure links start off (switchable), to avoid a hairball
const OFF_TYPES = new Set(["essay"]);
const OFF_KINDS = new Set(["wrote", "mentioned_in"]);

export function defaultFilters(): Filters {
  return {
    types: new Set(NODE_TYPES.filter((t) => !OFF_TYPES.has(t))),
    kinds: new Set(LINK_KINDS.filter((k) => !OFF_KINDS.has(k))),
    essay: null,
  };
}

export interface Visible {
  nodes: Set<string>;
  links: Set<number>; // indexes into graph.links
}

// a link shows when its kind is on, both ends' types are on, and (if an essay is picked) it comes
// from that essay. a node shows when its type is on and, under an essay filter, a shown link touches it.
// nothing else hides a link: weak links are shown as they are.
export function visible(g: KbGraph, f: Filters): Visible {
  const typeOf = new Map(g.nodes.map((n) => [n.id, n.type]));
  const links = new Set<number>();
  const touched = new Set<string>();
  g.links.forEach((l, i) => {
    if (!f.kinds.has(l.kind)) return;
    if (!f.types.has(typeOf.get(l.source)!) || !f.types.has(typeOf.get(l.target)!)) return;
    if (f.essay !== null && l.essay !== f.essay) return;
    links.add(i);
    touched.add(l.source);
    touched.add(l.target);
  });
  const nodes = new Set<string>();
  for (const n of g.nodes) {
    if (!f.types.has(n.type)) continue;
    if (f.essay !== null && !touched.has(n.id)) continue;
    nodes.add(n.id);
  }
  return { nodes, links };
}
