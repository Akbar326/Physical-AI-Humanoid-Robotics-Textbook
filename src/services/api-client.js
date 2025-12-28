/**
 * API Client Service for RAG Query Integration
 *
 * This service handles communication with the backend RAG API,
 * providing methods for submitting queries and handling responses.
 */

class ApiClient {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  /**
   * Submit a query to the RAG backend
   * @param {Object} queryData - The query data to send
   * @param {string} queryData.query - The natural language query from the user
   * @param {string} [queryData.selectedText] - Text selected by the user for context-aware queries
   * @param {number} [queryData.max_results=5] - Maximum number of context results to retrieve (1-20)
   * @param {boolean} [queryData.include_citations=true] - Whether to include source citations in response
   * @param {number} [queryData.temperature=0.3] - Controls response creativity (0.0-1.0)
   * @returns {Promise<Object>} The API response
   */
  async submitQuery(queryData, maxRetries = 2, timeout = 30000) {
    const {
      query,
      selectedText,
      max_results = 5,
      include_citations = true,
      temperature = 0.3
    } = queryData;

    // Validate input
    if (!query || typeof query !== 'string' || query.trim().length === 0) {
      throw new Error('Query is required and must be a non-empty string');
    }

    if (query.length > 1000) {
      throw new Error('Query must be between 1 and 1000 characters');
    }

    if (max_results < 1 || max_results > 20) {
      throw new Error('max_results must be between 1 and 20');
    }

    if (typeof include_citations !== 'boolean') {
      throw new Error('include_citations must be a boolean');
    }

    if (temperature < 0.0 || temperature > 1.0) {
      throw new Error('temperature must be between 0.0 and 1.0');
    }

    const requestBody = {
      query: query.trim(),
      ...(selectedText && { selectedText: selectedText.trim() }),
      max_results,
      include_citations,
      temperature
    };

    let lastError;

    // Attempt the request with retries for certain types of errors
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        // Create a timeout promise
        const timeoutPromise = new Promise((_, reject) => {
          setTimeout(() => {
            reject(new Error('Request timeout: The request took longer than expected'));
          }, timeout);
        });

        // Create the fetch promise
        const fetchPromise = fetch(`${this.baseURL}/api/v1/query`, {
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

  /**
   * Helper method to create a delay
   * @param {number} ms - Number of milliseconds to delay
   * @returns {Promise} A promise that resolves after the specified time
   */
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Check the health of the API server
   * @returns {Promise<Object>} The health check response
   */
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/api/v1/health`);

      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status} - ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the API server. Please check that the backend is running at http://localhost:8000');
      }
      throw error;
    }
  }
}

// Export a singleton instance of the API client
const apiClient = new ApiClient();
export default apiClient;