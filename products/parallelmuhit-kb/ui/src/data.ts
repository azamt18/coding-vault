import type { KbUrl } from "./urls";

// shape of extract/graph_grouped.json (built by the python pipeline, read-only here)

export const NODE_TYPES = ["person", "work", "idea", "organization", "theme", "author", "essay"] as const;
export const LINK_KINDS = [
  "recommends", "criticises", "inspired_by", "example_of", "counterexample_of",
  "associated_with", "in_theme", "wrote", "mentioned_in",
] as const;

export interface KbNode {
  id: string;
  label: string;
  type: string;
  aliases?: string[];
  descriptions?: Record<string, string>;
  essays?: string[];
  mention_count?: number;
  theme?: string;
  number?: number;
  slug?: string;
  source?: string;
  urls?: KbUrl[];
}

export interface KbLink {
  source: string;
  target: string;
  kind: string;
  essay?: string;
  label?: string;
  paragraph?: string;
  paragraphs?: string[];
  quote?: string;
  urls?: KbUrl[];
}

export interface KbGraph {
  nodes: KbNode[];
  links: KbLink[];
}

// the only place the data path lives; publishing later changes just this
export const DATA_URL = "/graph_grouped.json";

export function parseGraph(raw: unknown): KbGraph {
  const g = raw as Partial<KbGraph> | null;
  if (!g || !Array.isArray(g.nodes) || !Array.isArray(g.links)) {
    throw new Error("graph json needs 'nodes' and 'links' arrays");
  }
  const ids = new Set<string>();
  for (const n of g.nodes) {
    if (typeof n?.id !== "string" || typeof n.type !== "string") throw new Error(`bad node: ${JSON.stringify(n)}`);
    if (ids.has(n.id)) throw new Error(`duplicate node id: ${n.id}`);
    ids.add(n.id);
  }
  for (const l of g.links) {
    for (const end of [l?.source, l?.target]) {
      if (!ids.has(end)) throw new Error(`link endpoint is not a node: ${end}`);
    }
  }
  return { nodes: g.nodes, links: g.links };
}

export async function loadGraph(url: string = DATA_URL): Promise<KbGraph> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`could not load ${url}: ${res.status} (run sync_data.sh?)`);
  return parseGraph(await res.json());
}
