/**
 * RAG Integration Script
 *
 * This script provides direct JavaScript integration for RAG query functionality
 * that can be included in any HTML page without requiring a full React setup.
 */

class RagIntegration {
  constructor(options = {}) {
    this.options = {
      baseUrl: options.baseUrl || 'http://localhost:8000',
      containerId: options.containerId || 'rag-query-container',
      maxRetries: options.maxRetries || 2,
      timeout: options.timeout || 30000,
      ...options
    };

    this.container = null;
    this.queryInput = null;
    this.submitButton = null;
    this.resultContainer = null;
    this.loadingIndicator = null;

    this.init();
  }

  init() {
    this.container = document.getElementById(this.options.containerId);
    if (!this.container) {
      console.error(`Container with ID "${this.options.containerId}" not found`);
      return;
    }

    this.createUI();
    this.setupEventListeners();
  }

  createUI() {
    this.container.innerHTML = `
      <div class="rag-integration-container">
        <h3>Ask about the Content</h3>
        <div class="query-form">
          <textarea
            id="rag-query-input"
            placeholder="Ask a question about the content..."
            class="query-input"
            rows="3"
          ></textarea>
          <div class="form-actions">
            <button id="rag-submit-btn" class="submit-btn">Submit Query</button>
          </div>
        </div>
        <div id="rag-loading-indicator" class="loading-indicator" style="display: none;">
          <div class="spinner"></div>
          <span>Processing your query...</span>
        </div>
        <div id="rag-result-container" class="result-container"></div>
      </div>
    `;

    this.queryInput = document.getElementById('rag-query-input');
    this.submitButton = document.getElementById('rag-submit-btn');
    this.resultContainer = document.getElementById('rag-result-container');
    this.loadingIndicator = document.getElementById('rag-loading-indicator');
  }

  setupEventListeners() {
    this.submitButton.addEventListener('click', (e) => {
      e.preventDefault();
      this.handleQuerySubmit();
    });

    this.queryInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.handleQuerySubmit();
      }
    });
  }

  async handleQuerySubmit() {
    const query = this.queryInput.value.trim();
    if (!query) {
      this.displayError('Please enter a query');
      return;
    }

    if (query.length > 1000) {
      this.displayError('Query must be less than 1000 characters');
      return;
    }

    this.setLoading(true);

    try {
      // Get any selected text on the page
      const selectedText = this.getSelectedText();

      const queryData = {
        query: query,
        selectedText: selectedText || null,
        max_results: this.options.maxResults || 5,
        include_citations: this.options.includeCitations !== false, // default to true
        temperature: this.options.temperature || 0.3
      };

      const result = await this.submitQuery(queryData);
      this.displayResult(result);
    } catch (error) {
      this.displayError(error.message || 'An error occurred while processing your query');
    } finally {
      this.setLoading(false);
    }
  }

  async submitQuery(queryData, maxRetries = this.options.maxRetries) {
    // Validate input
    if (!queryData.query || typeof queryData.query !== 'string' || queryData.query.trim().length === 0) {
      throw new Error('Query is required and must be a non-empty string');
    }

    if (queryData.query.length > 1000) {
      throw new Error('Query must be between 1 and 1000 characters');
    }

    const maxResults = queryData.max_results || 5;
    if (maxResults < 1 || maxResults > 20) {
      throw new Error('max_results must be between 1 and 20');
    }

    const requestBody = {
      query: queryData.query.trim(),
      ...(queryData.selectedText && { selectedText: queryData.selectedText.trim() }),
      max_results: maxResults,
      include_citations: queryData.include_citations !== false,
      temperature: queryData.temperature || 0.3
    };

    let lastError;

    // Attempt the request with retries for certain types of errors
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        // Create a timeout promise
        const timeoutPromise = new Promise((_, reject) => {
          setTimeout(() => {
            reject(new Error('Request timeout: The request took longer than expected'));
          }, this.options.timeout);
        });

        // Create the fetch promise
        const fetchPromise = fetch(`${this.options.baseUrl}/api/v1/query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody)
        });

        // Race between the fetch and timeout promises
        const response = await Promise.race([fetchPromise, timeoutPromise]);

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));

          // Handle specific error codes from the API
          if (response.status === 400) {
            throw new Error(`Invalid query: ${errorData.detail || 'Bad request'}`);
          } else if (response.status === 422) {
            throw new Error(`Validation error: ${errorData.detail || 'Unprocessable entity'}`);
          } else if (response.status === 429) {
            throw new Error(`Rate limit exceeded: ${errorData.detail || 'Too many requests'}`);
          } else if (response.status === 500) {
            throw new Error(`Server error: ${errorData.detail || 'Internal server error'}`);
          } else {
            // For 5xx errors and network errors, we might want to retry
            if (response.status >= 500 || response.status === 408 || response.status === 429) {
              if (attempt < maxRetries) {
                // Wait before retrying (exponential backoff)
                const waitTime = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s...
                await this.delay(waitTime);
                continue;
              }
            }
            throw new Error(`API request failed: ${response.status} - ${errorData.detail || response.statusText}`);
          }
        }

        const data = await response.json();
        return data;
      } catch (error) {
        lastError = error;

        // Check if this is a timeout error or network error that might be retried
        if (error.message.includes('timeout') ||
            (error.name === 'TypeError' && (error.message.includes('fetch') || error.message.includes('Failed to fetch')))) {
          if (attempt < maxRetries) {
            // Wait before retrying (exponential backoff)
            const waitTime = Math.pow(2, attempt) * 1000; // 1s, 2s, 4s...
            await this.delay(waitTime);
            continue;
          }
        }

        // If it's a client error (4xx), don't retry
        if (error.message.includes('Invalid query') || error.message.includes('Validation error')) {
          throw error;
        }
      }
    }

    // If we've exhausted retries, throw the last error
    throw lastError;
  }

  getSelectedText() {
    const selection = window.getSelection ? window.getSelection() : document.selection;
    if (selection) {
      return selection.toString().trim();
    }
    return '';
  }

  setLoading(loading) {
    if (loading) {
      this.submitButton.disabled = true;
      this.submitButton.textContent = 'Submitting...';
      this.loadingIndicator.style.display = 'flex';
    } else {
      this.submitButton.disabled = false;
      this.submitButton.textContent = 'Submit Query';
      this.loadingIndicator.style.display = 'none';
    }
  }

  displayResult(result) {
    if (!result || typeof result !== 'object') {
      this.displayError('Invalid response from API');
      return;
    }

    let html = '<div class="result-content">';

    html += '<div class="answer-section">';
    html += '<h4>Answer</h4>';
    html += `<div class="answer">${this.escapeHtml(result.answer || 'No answer provided.')}</div>`;
    html += '</div>';

    if (result.citations && Array.isArray(result.citations) && result.citations.length > 0) {
      html += '<div class="citations-section">';
      html += '<h4>Sources</h4>';
      html += '<ul class="citations-list">';
      result.citations.forEach(citation => {
        html += `<li class="citation-item">
          <a href="${this.escapeHtml(citation.url || '#')}" target="_blank" rel="noopener noreferrer">
            ${this.escapeHtml(citation.title || 'Untitled')}
          </a>
          ${citation.score ? `<span class="citation-score">Relevance: ${(citation.score * 100).toFixed(1)}%</span>` : ''}
        </li>`;
      });
      html += '</ul>';
      html += '</div>';
    }

    if (result.retrieved_contexts && Array.isArray(result.retrieved_contexts) && result.retrieved_contexts.length > 0) {
      html += '<div class="contexts-section">';
      html += '<h4>Retrieved Context</h4>';
      result.retrieved_contexts.forEach(context => {
        html += `<div class="context-item">
          <h5><a href="${this.escapeHtml(context.url || '#')}" target="_blank" rel="noopener noreferrer">${this.escapeHtml(context.title || 'Untitled')}</a></h5>
          <p>${this.escapeHtml(context.content || '')}</p>
          ${context.score ? `<span class="context-score">Score: ${(context.score * 100).toFixed(1)}%</span>` : ''}
        </div>`;
      });
      html += '</div>';
    }

    if (result.execution_time) {
      html += `<div class="execution-info">
        <small>Response time: ${Number(result.execution_time).toFixed(2)} seconds</small>
      </div>`;
    }

    html += '</div>';

    this.resultContainer.innerHTML = html;
  }

  displayError(message) {
    this.resultContainer.innerHTML = `
      <div class="error-message">
        <h4>Error</h4>
        <p>${this.escapeHtml(message)}</p>
      </div>
    `;
  }

  escapeHtml(text) {
    if (typeof text !== 'string') return '';
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Auto-initialize if the script is included with data attributes
document.addEventListener('DOMContentLoaded', function() {
  const containers = document.querySelectorAll('[data-rag-integration]');
  containers.forEach(container => {
    const containerId = container.id || `rag-container-${Date.now()}`;
    if (!container.id) {
      container.id = containerId;
    }

    const options = {
      containerId: containerId,
      baseUrl: container.dataset.baseUrl,
      maxResults: parseInt(container.dataset.maxResults) || undefined,
      includeCitations: container.dataset.includeCitations !== 'false',
      temperature: parseFloat(container.dataset.temperature) || undefined
    };

    // Remove undefined values
    Object.keys(options).forEach(key => {
      if (options[key] === undefined) delete options[key];
    });

    new RagIntegration(options);
  });
});

// Make RagIntegration available globally
window.RagIntegration = RagIntegration;