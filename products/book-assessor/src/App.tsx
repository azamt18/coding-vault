import { useCallback, useEffect, useState } from "react";
import { useAssessment } from "./hooks";
import { BookLoader } from "./components/BookLoader";
import { AssessmentFlow } from "./components/AssessmentFlow";
import { ReportView } from "./components/ReportView";
import bank from "./data/anxious-generation.json";
import type { QuestionBank } from "./types";

type Step = "loading" | "assessing" | "report";

const questionBank = bank as unknown as QuestionBank;

/**
 * root component: loading -> assessing -> report.
 */
export default function App() {
  const {
    book,
    setBook,
    questions,
    setQuestions,
    answers,
    result,
    setAnswer,
    runAssessment,
    reset,
  } = useAssessment();
  const [step, setStep] = useState<Step>("loading");

  // load the question bank once on mount
  useEffect(() => {
    setQuestions(questionBank);
  }, [setQuestions]);

  // move on once the book has loaded
  useEffect(() => {
    if (step === "loading" && book) setStep("assessing");
  }, [step, book]);

  // move to the report once the assessment produced a result
  useEffect(() => {
    if (step === "assessing" && result) setStep("report");
  }, [step, result]);

  const handleLoaded = useCallback(setBook, [setBook]);

  // reset clears the question bank too, so put it back
  const startOver = () => {
    reset();
    setQuestions(questionBank);
    setStep("loading");
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>kitoblab</h1>
        {book && (
          <p className="app-subtitle">
            {book.title} by {book.author}
          </p>
        )}
      </header>

      {step === "loading" && <BookLoader onLoaded={handleLoaded} />}

      {step === "assessing" && (
        <AssessmentFlow
          questions={questions}
          chapters={book?.chapters ?? []}
          answers={answers}
          setAnswer={setAnswer}
          runAssessment={runAssessment}
        />
      )}

      {step === "report" && result && (
        <ReportView result={result} questions={questions} />
      )}

      {step !== "loading" && (
        <button type="button" className="start-over" onClick={startOver}>
          start over
        </button>
      )}
    </div>
  );
}
