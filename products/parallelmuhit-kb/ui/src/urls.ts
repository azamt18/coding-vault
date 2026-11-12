// links to the pages the author linked from an essay (graph `urls`); pure so it tests without a DOM
export interface KbUrl {
  text: string;
  url: string;
}

export interface UrlItem {
  href: string;
  label: string;
  target: "_blank";
  rel: "noopener noreferrer";
}

// nothing when there are no urls; only http(s) is ever rendered as a link
export function urlItems(urls?: KbUrl[]): UrlItem[] {
  return (urls ?? [])
    .filter((u) => /^https?:\/\//i.test(u.url))
    .map((u) => ({ href: u.url, label: `↗ ${u.text || u.url}`, target: "_blank", rel: "noopener noreferrer" }));
}
