import React, { useState } from 'react';
import clsx from 'clsx';

interface ExerciseStep {
  id: number;
  description: string;
  command?: string;
  expectedOutput?: string;
}

interface ExerciseProps {
  title: string;
  description: string;
  steps: ExerciseStep[];
  timeEstimate?: string;
  difficulty?: 'Beginner' | 'Intermediate' | 'Advanced';
  showSolution?: boolean;
  solution?: string;
  solutionTitle?: string;
}

/**
 * Exercise Component
 * Provides a structured exercise with steps and solution toggle
 */
const Exercise: React.FC<ExerciseProps> = ({
  title,
  description,
  steps,
  timeEstimate,
  difficulty,
  showSolution = true,
  solution,
  solutionTitle = 'Solution and Explanation'
}) => {
  const [showSolutionContent, setShowSolutionContent] = useState(false);

  const toggleSolution = () => {
    setShowSolutionContent(!showSolutionContent);
  };

  const difficultyClasses = clsx(
    'exercise__difficulty',
    {
      'exercise__difficulty--beginner': difficulty === 'Beginner',
      'exercise__difficulty--intermediate': difficulty === 'Intermediate',
      'exercise__difficulty--advanced': difficulty === 'Advanced',
    }
  );

  return (
    <div className="exercise margin-bottom--lg border-radius--md">
      <div className="exercise__header padding--md background--primary">
        <h3 className="exercise__title margin-bottom--sm">{title}</h3>
        <p className="exercise__description margin-bottom--sm">{description}</p>

        <div className="exercise__meta">
          {timeEstimate && (
            <span className="exercise__time badge badge--secondary margin-right--sm">
              ⏱️ {timeEstimate}
            </span>
          )}
          {difficulty && (
            <span className={difficultyClasses}>
              {difficulty}
            </span>
          )}
        </div>
      </div>

      <div className="exercise__body padding--md">
        <h4 className="exercise__steps-title">Steps:</h4>
        <ol className="exercise__steps-list">
          {steps.map((step) => (
            <li key={step.id} className="exercise__step margin-bottom--md">
              <div className="exercise__step-description">
                {step.description}
              </div>
              {step.command && (
                <div className="exercise__step-command margin-top--sm">
                  <pre className="code-block">
                    <code className="language-bash">{step.command}</code>
                  </pre>
                </div>
              )}
              {step.expectedOutput && (
                <div className="exercise__step-output margin-top--sm">
                  <h6>Expected Output:</h6>
                  <pre className="code-block">
                    <code>{step.expectedOutput}</code>
                  </pre>
                </div>
              )}
            </li>
          ))}
        </ol>
      </div>

      {showSolution && solution && (
        <div className="exercise__solution padding--md">
          <button
            className="button button--outline button--primary margin-bottom--md"
            onClick={toggleSolution}
          >
            {showSolutionContent ? 'Hide Solution' : 'Show Solution'}
          </button>

          {showSolutionContent && (
            <div className="exercise__solution-content">
              <h4 className="exercise__solution-title">{solutionTitle}</h4>
              <div className="exercise__solution-body">
                {solution}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Exercise;