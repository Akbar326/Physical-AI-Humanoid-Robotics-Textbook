/**
 * RagQueryContext Component
 *
 * This component provides context and state management for the RAG query system.
 * It manages the communication between the form and result components,
 * handles API calls, and manages loading/error states.
 */

import React, { useState, useEffect } from 'react';
import RagQueryForm from './RagQueryForm';
import RagQueryResult from './RagQueryResult';
import apiClient from '../../services/api-client';
import { getSelectedText, addTextSelectionListener, sanitizeSelectedText } from '../../utils/text-selection';

const RagQueryContext = () => {
  const [queryResult, setQueryResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedText, setSelectedText] = useState('');

  // Listen for text selection changes at the context level as well
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

  const handleQuerySubmit = async (queryData) => {
    setIsLoading(true);
    setError('');
    setQueryResult(null);

    try {
      const result = await apiClient.submitQuery(queryData);

      // Validate the result structure
      if (!result || typeof result !== 'object') {
        throw new Error('Invalid response from API');
      }

      setQueryResult(result);
    } catch (err) {
      console.error('Error submitting query:', err);
      setError(err.message || 'An error occurred while processing your query');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="rag-query-context-container">
      <h2>Ask about the Book Content</h2>
      {selectedText && (
        <div className="context-info">
          <small>Selected text context: "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</small>
        </div>
      )}
      <RagQueryForm onSubmitQuery={handleQuerySubmit} />
      <RagQueryResult
        result={queryResult}
        loading={isLoading}
        error={error}
      />
    </div>
  );
};

export default RagQueryContext;