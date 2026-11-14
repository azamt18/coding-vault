import { useMemo } from "react";
import type { AssessmentResult, QuestionBank } from "../types";
import { formatReport } from "../utils/markdown";

interface ReportViewProps {
  result: AssessmentResult;
  questions: QuestionBank;
}

// lowercase, hyphen-separated filename based on the book title
function fileNameFor(title: string): string {
  const slug = title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return `${slug || "book"}-reading-plan.md`;
}

/**
 * shows the markdown report and lets the user download it as a .md file.
 */
export function ReportView({ result, questions }: ReportViewProps) {
  const markdown = useMemo(() => formatReport(result, questions), [result, questions]);

  // save the exact markdown string via a blob url, then revoke the url
  const handleDownload = () => {
    const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = fileNameFor(result.book.title);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <section>
      <button type="button" onClick={handleDownload} style={{ marginBottom: 12 }}>
        download report (.md)
      </button>
      <pre
        style={{
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
          padding: 12,
          border: "1px solid #ccc",
          borderRadius: 4,
        }}
      >
        {markdown}
      </pre>
    </section>
  );
}
