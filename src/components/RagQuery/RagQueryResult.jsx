/**
 * RagQueryResult Component
 *
 * This component displays the results from the RAG query API,
 * including the answer, citations, and retrieved contexts.
 */

import React from 'react';

const RagQueryResult = ({ result, loading, error }) => {
  if (loading) {
    return (
      <div className="rag-query-result-container">
        <div className="loading-indicator">
          <div className="spinner"></div>
          <p>Processing your query...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rag-query-result-container">
        <div className="error-message">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="rag-query-result-container">
        <div className="empty-state">
          <p>Submit a query to see results here.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="rag-query-result-container">
      <div className="query-result-content">
        <div className="answer-section">
          <h3>Answer</h3>
          <div className="answer-content">
            {result.answer ? (
              <p>{result.answer}</p>
            ) : (
              <p>No answer provided.</p>
            )}
          </div>
        </div>

        {result.citations && result.citations.length > 0 && (
          <div className="citations-section">
            <h3>Sources</h3>
            <ul className="citations-list">
              {result.citations.map((citation, index) => (
                <li key={index} className="citation-item">
                  <a href={citation.url} target="_blank" rel="noopener noreferrer">
                    {citation.title}
                  </a>
                  <span className="citation-score">Relevance: {(citation.score * 100).toFixed(1)}%</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {result.retrieved_contexts && result.retrieved_contexts.length > 0 && (
          <div className="contexts-section">
            <h3>Retrieved Context</h3>
            <div className="contexts-list">
              {result.retrieved_contexts.map((context, index) => (
                <div key={index} className="context-item">
                  <h4>
                    <a href={context.url} target="_blank" rel="noopener noreferrer">
                      {context.title}
                    </a>
                  </h4>
                  <p>{context.content}</p>
                  <span className="context-score">Score: {(context.score * 100).toFixed(1)}%</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {result.execution_time && (
          <div className="execution-info">
            <small>Response time: {result.execution_time.toFixed(2)} seconds</small>
          </div>
        )}
      </div>

      <style jsx>{`
        .rag-query-result-container {
          margin: 20px 0;
          padding: 20px;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          background-color: #ffffff;
        }

        .loading-indicator {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 40px 20px;
        }

        .spinner {
          width: 40px;
          height: 40px;
          border: 4px solid #f3f3f3;
          border-top: 4px solid #2196f3;
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin-bottom: 15px;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .error-message {
          padding: 20px;
          background-color: #ffebee;
          color: #c62828;
          border: 1px solid #ffcdd2;
          border-radius: 4px;
        }

        .error-message h3 {
          margin-top: 0;
          color: #c62828;
        }

        .empty-state {
          padding: 40px 20px;
          text-align: center;
          color: #757575;
        }

        .query-result-content {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .answer-section h3,
        .citations-section h3,
        .contexts-section h3 {
          margin-top: 0;
          color: #333;
          border-bottom: 1px solid #e0e0e0;
          padding-bottom: 8px;
        }

        .answer-content {
          padding: 15px 0;
          line-height: 1.6;
        }

        .citations-list {
          list-style: none;
          padding: 0;
        }

        .citations-list li {
          margin-bottom: 10px;
          padding: 8px;
          background-color: #f5f5f5;
          border-radius: 4px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
        }

        .citation-item a {
          color: #2196f3;
          text-decoration: none;
          flex-grow: 1;
        }

        .citation-item a:hover {
          text-decoration: underline;
        }

        .citation-score {
          color: #757575;
          font-size: 0.9em;
          margin-left: 10px;
        }

        .contexts-list {
          display: flex;
          flex-direction: column;
          gap: 15px;
        }

        .context-item {
          padding: 15px;
          border: 1px solid #e0e0e0;
          border-radius: 4px;
          background-color: #fafafa;
        }

        .context-item h4 {
          margin-top: 0;
          margin-bottom: 10px;
        }

        .context-item h4 a {
          color: #2196f3;
          text-decoration: none;
        }

        .context-item h4 a:hover {
          text-decoration: underline;
        }

        .context-item p {
          margin: 10px 0;
          color: #555;
        }

        .context-score {
          display: block;
          text-align: right;
          color: #757575;
          font-size: 0.9em;
        }

        .execution-info {
          text-align: right;
          color: #757575;
          font-size: 0.9em;
          padding-top: 10px;
          border-top: 1px solid #e0e0e0;
        }
      `}</style>
    </div>
  );
};

export default RagQueryResult;