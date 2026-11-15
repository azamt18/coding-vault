import type { Question } from "../types";

interface QuestionCardProps {
  question: Question;
  selected?: string;
  onAnswer: (choice: string) => void;
}

const LETTERS = ["A", "B", "C", "D"];

/**
 * shows one question with lettered options and reports the chosen letter.
 */
export function QuestionCard({ question, selected, onAnswer }: QuestionCardProps) {
  return (
    <fieldset style={{ marginBottom: 16 }}>
      <legend>{question.prompt}</legend>
      {question.options.map((option, i) => {
        const letter = LETTERS[i] ?? String(i);
        const isSelected = selected === letter;
        return (
          <label
            key={letter}
            style={{ display: "block", fontWeight: isSelected ? "bold" : "normal" }}
          >
            <input
              type="radio"
              name={question.id}
              value={letter}
              checked={isSelected}
              onChange={() => onAnswer(letter)}
            />{" "}
            {letter}. {option}
          </label>
        );
      })}
    </fieldset>
  );
}
