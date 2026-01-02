/**
 * RagQueryForm Component
 *
 * This component provides a form for users to submit queries about book content.
 * It integrates with the API client and text selection utilities to enable
 * both basic and context-aware queries.
 */

import React, { useState, useEffect } from 'react';
import { getSelectedText, addTextSelectionListener, sanitizeSelectedText } from '../../utils/text-selection';

const RagQueryForm = ({ onSubmitQuery }) => {
  const [query, setQuery] = useState('');
  const [selectedText, setSelectedText] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  // Listen for text selection changes
  useEffect(() => {
    const removeListener = addTextSelectionListener((selectionInfo) => {
      if (selectionInfo) {
        const sanitizedText = sanitizeSelectedText(selectionInfo.text);
        setSelectedText(sanitizedText);
      } else {
        setSelectedText('');
      }
    });

    return removeListener;
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!query.trim()) {
      setError('Please enter a query');
      return;
    }

    if (query.trim().length > 1000) {
      setError('Query must be less than 1000 characters');
      return;
    }

    setIsSubmitting(true);
    setError('');

    try {
      // Prepare query data
      const queryData = {
        query: query.trim(),
        selectedText: selectedText || null
      };

      // Submit the query via the callback
      await onSubmitQuery(queryData);

      // Clear the form after successful submission
      setQuery('');
    } catch (err) {
      setError(err.message || 'An error occurred while submitting the query');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="rag-query-form-container">
      <form onSubmit={handleSubmit} className="rag-query-form">
        {selectedText && (
          <div className="selected-text-preview">
            <small>Context: "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</small>
          </div>
        )}

        <div className="query-input-container">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about the book content..."
            className="query-input"
            rows="3"
            disabled={isSubmitting}
          />
        </div>

        <div className="form-actions">
          <button
            type="submit"
            disabled={isSubmitting || !query.trim()}
            className="submit-button"
          >
            {isSubmitting ? 'Submitting...' : 'Submit Query'}
          </button>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
      </form>

      <style jsx>{`
        .rag-query-form-container {
          margin: 20px 0;
          padding: 20px;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          background-color: #fafafa;
        }

        .rag-query-form {
          display: flex;
          flex-direction: column;
          gap: 15px;
        }

        .selected-text-preview {
          padding: 10px;
          background-color: #e3f2fd;
          border-left: 3px solid #2196f3;
          border-radius: 4px;
        }

        .query-input-container {
          width: 100%;
        }

        .query-input {
          width: 100%;
          padding: 12px;
          border: 1px solid #ccc;
          border-radius: 4px;
          font-size: 16px;
          resize: vertical;
          min-height: 80px;
        }

        .query-input:focus {
          outline: none;
          border-color: #2196f3;
          box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
        }

        .form-actions {
          display: flex;
          justify-content: flex-start;
        }

        .submit-button {
          padding: 10px 20px;
          background-color: #2196f3;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 16px;
          transition: background-color 0.3s;
        }

        .submit-button:hover:not(:disabled) {
          background-color: #0d8bf2;
        }

        .submit-button:disabled {
          background-color: #bbdefb;
          cursor: not-allowed;
        }

        .error-message {
          padding: 10px;
          background-color: #ffebee;
          color: #c62828;
          border: 1px solid #ffcdd2;
          border-radius: 4px;
          margin-top: 10px;
        }
      `}</style>
    </div>
  );
};

export default RagQueryForm;