import type { Chapter, QuestionBank } from "../types";
import { QuestionCard } from "./QuestionCard";

interface AssessmentFlowProps {
  questions: QuestionBank;
  chapters: Chapter[];
  answers: Record<string, string>;
  setAnswer: (questionId: string, answer: string) => void;
  runAssessment: () => void;
}

/**
 * batch flow: all questions listed chapter by chapter, run is gated on every one being answered.
 */
export function AssessmentFlow({
  questions,
  chapters: bookChapters,
  answers,
  setAnswer,
  runAssessment,
}: AssessmentFlowProps) {
  const chapters = Object.keys(questions)
    .map(Number)
    .sort((a, b) => a - b);
  const titleOf = (n: number) =>
    bookChapters.find((ch) => ch.number === n)?.title.toLowerCase();
  const all = chapters.flatMap((c) => questions[c] ?? []);
  const answered = all.filter((q) => answers[q.id] !== undefined).length;
  const complete = all.length > 0 && answered === all.length;

  return (
    <div>
      <p>
        answered {answered} of {all.length}
      </p>
      {chapters.map((c) => (
        <section key={c}>
          <h3>
            chapter {c}
            {titleOf(c) ? `: ${titleOf(c)}` : ""}
          </h3>
          {(questions[c] ?? []).map((q) => (
            <QuestionCard
              key={q.id}
              question={q}
              selected={answers[q.id]}
              onAnswer={(choice) => setAnswer(q.id, choice)}
            />
          ))}
        </section>
      ))}
      <button type="button" disabled={!complete} onClick={runAssessment}>
        run assessment
      </button>
    </div>
  );
}
