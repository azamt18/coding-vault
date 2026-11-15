import type { AssessmentResult, QuestionBank } from "../types";

const pct = (score: number): string => `${Math.round(score * 100)}%`;

/**
 * Builds a hybrid markdown report: compact table up top, then one
 * expandable <details> section per chapter. All output is lowercased.
 * Pass `questions` to include each question with the user's answer.
 */
export function formatReport(
  result: AssessmentResult,
  questions?: QuestionBank
): string {
  const titleOf = (n: number): string =>
    result.book.chapters.find((c) => c.number === n)?.title ?? `chapter ${n}`;

  const lines: string[] = [
    `# ${result.book.title} - reading plan`,
    "",
    "| chapter | score | recommendation |",
    "| --- | --- | --- |",
    ...result.scores.map(
      (s) =>
        `| ${s.chapter}. ${titleOf(s.chapter)} | ${pct(s.score)} | ${s.recommendation} |`
    ),
    "",
  ];

  for (const s of result.scores) {
    lines.push(
      "<details>",
      `<summary>${s.chapter}. ${titleOf(s.chapter)} - ${pct(s.score)} - ${s.recommendation}</summary>`,
      "",
      `- score: ${pct(s.score)}`,
      `- recommendation: ${s.recommendation}`
    );
    for (const q of questions?.[s.chapter] ?? []) {
      const given = result.answers[q.id] ?? "no answer";
      const mark = given === q.correctAnswer ? "correct" : "incorrect";
      lines.push(
        `- ${q.prompt}`,
        `  - your answer: ${given} (${mark}), correct: ${q.correctAnswer}`
      );
    }
    lines.push("", "</details>", "");
  }

  return lines.join("\n").toLowerCase();
}
