import { useCallback, useState } from "react";
import type { AssessmentResult, Book, QuestionBank } from "../types";
import { scoreAssessment } from "../utils/scoring";

/**
 * holds assessment state: book, question bank, answers (keyed by question id) and result.
 */
export function useAssessment() {
  const [book, setBook] = useState<Book | null>(null);
  const [questions, setQuestions] = useState<QuestionBank>({});
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<AssessmentResult | null>(null);

  const setAnswer = useCallback((questionId: string, answer: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: answer }));
  }, []);

  // no-op until a book is set, since the result needs one
  const runAssessment = useCallback(() => {
    if (!book) return;
    setResult({ book, scores: scoreAssessment(questions, answers), answers });
  }, [book, questions, answers]);

  const reset = useCallback(() => {
    setBook(null);
    setQuestions({});
    setAnswers({});
    setResult(null);
  }, []);

  return {
    book,
    setBook,
    questions,
    setQuestions,
    answers,
    result,
    setAnswer,
    runAssessment,
    reset,
  };
}
