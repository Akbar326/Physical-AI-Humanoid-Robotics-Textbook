/**
 * Query History Utilities
 *
 * This utility provides functions for managing query history
 * to allow users to review previous queries and responses.
 */

// Maximum number of queries to store in history
const MAX_HISTORY_SIZE = 50;

/**
 * Get query history from localStorage
 * @returns {Array} Array of query history items
 */
export function getQueryHistory() {
  try {
    const history = localStorage.getItem('ragQueryHistory');
    if (history) {
      return JSON.parse(history);
    }
    return [];
  } catch (error) {
    console.error('Error reading query history from localStorage:', error);
    return [];
  }
}

/**
 * Save query history to localStorage
 * @param {Array} history - Array of query history items to save
 */
export function saveQueryHistory(history) {
  try {
    // Keep only the most recent queries up to the maximum size
    const trimmedHistory = history.slice(0, MAX_HISTORY_SIZE);
    localStorage.setItem('ragQueryHistory', JSON.stringify(trimmedHistory));
  } catch (error) {
    console.error('Error saving query history to localStorage:', error);
  }
}

/**
 * Add a query to the history
 * @param {Object} queryData - The query data to add
 * @param {Object} response - The response received
 */
export function addQueryToHistory(queryData, response) {
  const history = getQueryHistory();

  const historyItem = {
    id: Date.now().toString(), // Use timestamp as unique ID
    timestamp: new Date().toISOString(),
    query: queryData.query,
    selectedText: queryData.selectedText || null,
    response: response || null,
    responseTime: response?.execution_time || null
  };

  // Add the new item to the beginning of the array
  const updatedHistory = [historyItem, ...history];

  // Save the updated history
  saveQueryHistory(updatedHistory);
}

/**
 * Remove a query from history by ID
 * @param {string} id - The ID of the query to remove
 */
export function removeQueryFromHistory(id) {
  const history = getQueryHistory();
  const updatedHistory = history.filter(item => item.id !== id);
  saveQueryHistory(updatedHistory);
}

/**
 * Clear all query history
 */
export function clearQueryHistory() {
  localStorage.removeItem('ragQueryHistory');
}

/**
 * Get recent queries (last N queries)
 * @param {number} count - Number of recent queries to return (default 10)
 * @returns {Array} Array of recent query history items
 */
export function getRecentQueries(count = 10) {
  const history = getQueryHistory();
  return history.slice(0, count);
}

/**
 * Search queries by text content
 * @param {string} searchTerm - Text to search for in queries
 * @returns {Array} Array of matching query history items
 */
export function searchQueryHistory(searchTerm) {
  if (!searchTerm) return [];

  const history = getQueryHistory();
  const lowerSearchTerm = searchTerm.toLowerCase();

  return history.filter(item =>
    item.query.toLowerCase().includes(lowerSearchTerm) ||
    (item.selectedText && item.selectedText.toLowerCase().includes(lowerSearchTerm)) ||
    (item.response?.answer && item.response.answer.toLowerCase().includes(lowerSearchTerm))
  );
}

/**
 * QueryHistory React component for displaying history
 */
import React, { useState, useEffect } from 'react';

export const QueryHistoryPanel = ({ onSelectQuery }) => {
  const [history, setHistory] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isPanelOpen, setIsPanelOpen] = useState(false);

  useEffect(() => {
    setHistory(getQueryHistory());
  }, []);

  const filteredHistory = searchTerm
    ? searchQueryHistory(searchTerm)
    : history;

  const handleSelectQuery = (queryItem) => {
    if (onSelectQuery) {
      onSelectQuery({
        query: queryItem.query,
        selectedText: queryItem.selectedText
      });
    }
    setIsPanelOpen(false);
  };

  const handleClearHistory = () => {
    clearQueryHistory();
    setHistory([]);
    setSearchTerm('');
  };

  return (
    <div className="query-history-panel">
      <button
        className="history-toggle-btn"
        onClick={() => setIsPanelOpen(!isPanelOpen)}
      >
        {isPanelOpen ? 'Hide History' : 'Show History'} ({history.length})
      </button>

      {isPanelOpen && (
        <div className="history-content">
          <div className="history-controls">
            <input
              type="text"
              placeholder="Search queries..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="history-search"
            />
            <button
              className="clear-history-btn"
              onClick={handleClearHistory}
              disabled={history.length === 0}
            >
              Clear All
            </button>
          </div>

          <div className="history-list">
            {filteredHistory.length === 0 ? (
              <div className="no-history">
                {searchTerm ? 'No matching queries found' : 'No query history yet'}
              </div>
            ) : (
              filteredHistory.map((item) => (
                <div key={item.id} className="history-item">
                  <div className="history-query" onClick={() => handleSelectQuery(item)}>
                    <div className="query-text">{item.query}</div>
                    {item.selectedText && (
                      <div className="selected-text-preview">"{item.selectedText.substring(0, 50)}{item.selectedText.length > 50 ? '...' : ''}"</div>
                    )}
                    <div className="history-meta">
                      <span className="timestamp">
                        {new Date(item.timestamp).toLocaleString()}
                      </span>
                      {item.responseTime && (
                        <span className="response-time">{item.responseTime}s</span>
                      )}
                    </div>
                  </div>
                  <button
                    className="remove-item-btn"
                    onClick={(e) => {
                      e.stopPropagation();
                      removeQueryFromHistory(item.id);
                      setHistory(getQueryHistory());
                    }}
                  >
                    Remove
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      <style jsx>{`
        .query-history-panel {
          margin-top: 10px;
        }

        .history-toggle-btn {
          background-color: #f5f5f5;
          border: 1px solid #ddd;
          padding: 8px 12px;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
        }

        .history-toggle-btn:hover {
          background-color: #e0e0e0;
        }

        .history-content {
          margin-top: 10px;
          border: 1px solid #ddd;
          border-radius: 4px;
          background-color: #fafafa;
          max-height: 400px;
          overflow-y: auto;
        }

        .history-controls {
          padding: 10px;
          border-bottom: 1px solid #ddd;
          display: flex;
          gap: 10px;
        }

        .history-search {
          flex: 1;
          padding: 5px;
          border: 1px solid #ccc;
          border-radius: 3px;
        }

        .clear-history-btn {
          padding: 5px 10px;
          background-color: #ff6b6b;
          color: white;
          border: none;
          border-radius: 3px;
          cursor: pointer;
        }

        .clear-history-btn:disabled {
          background-color: #cccccc;
          cursor: not-allowed;
        }

        .history-list {
          padding: 10px;
        }

        .no-history {
          text-align: center;
          color: #777;
          padding: 20px;
        }

        .history-item {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          padding: 10px;
          border-bottom: 1px solid #eee;
        }

        .history-query {
          flex: 1;
          cursor: pointer;
        }

        .history-query:hover {
          background-color: #e3f2fd;
          border-radius: 3px;
          padding: 5px;
        }

        .query-text {
          font-weight: 500;
          margin-bottom: 5px;
        }

        .selected-text-preview {
          font-size: 0.9em;
          color: #555;
          margin-bottom: 5px;
          padding: 3px 5px;
          background-color: #e8f4fd;
          border-radius: 3px;
          display: inline-block;
        }

        .history-meta {
          font-size: 0.8em;
          color: #777;
          display: flex;
          gap: 10px;
        }

        .remove-item-btn {
          background-color: #ff6b6b;
          color: white;
          border: none;
          border-radius: 3px;
          padding: 4px 8px;
          cursor: pointer;
          font-size: 0.8em;
          align-self: flex-start;
          margin-top: 5px;
        }

        .remove-item-btn:hover {
          background-color: #ff5252;
        }
      `}</style>
    </div>
  );
};