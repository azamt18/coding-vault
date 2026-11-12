import type { KbGraph } from "./data";

// small hand-made graph shaped like extract/graph_grouped.json
export function fixture(): KbGraph {
  return {
    nodes: [
      { id: "author:aziz-rahimov", label: "Aziz Rahimov", type: "author" },
      { id: "essay:001_a", label: "Essay A", type: "essay", number: 1, slug: "a", source: "https://x/a" },
      { id: "essay:002_b", label: "Essay B", type: "essay", number: 2, slug: "b", source: "https://x/b" },
      {
        id: "person:munger", label: "Charli Manger", type: "person",
        aliases: ["Charlie Munger", "Munger"], descriptions: { "001_a": "investor" },
        essays: ["001_a"], mention_count: 3,
      },
      {
        id: "idea:o'qish", label: "O‘qish", type: "idea", aliases: [],
        descriptions: { "001_a": "reading", "002_b": "reading again" },
        essays: ["001_a", "002_b"], mention_count: 2, theme: "Bilim",
      },
      { id: "work:kitob", label: "Kitob", type: "work", aliases: [], descriptions: {}, essays: ["002_b"], mention_count: 1 },
      { id: "theme:bilim", label: "Bilim", type: "theme" },
    ],
    links: [
      { source: "author:aziz-rahimov", target: "essay:001_a", kind: "wrote", essay: "001_a" },
      { source: "person:munger", target: "essay:001_a", kind: "mentioned_in", essay: "001_a", paragraphs: ["p1"] },
      { source: "person:munger", target: "idea:o'qish", kind: "recommends", essay: "001_a", paragraph: "p2", quote: "O‘qing.", label: "reads" },
      { source: "work:kitob", target: "idea:o'qish", kind: "example_of", essay: "002_b", paragraph: "p3", quote: "Kitob." },
      { source: "person:munger", target: "work:kitob", kind: "criticises", essay: "002_b", paragraph: "p4", quote: "Yomon." },
      { source: "idea:o'qish", target: "theme:bilim", kind: "in_theme" },
    ],
  };
}
