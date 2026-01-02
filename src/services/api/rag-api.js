/**
 * API utility functions for RAG (Retrieval-Augmented Generation) integration
 * Provides functions to interact with the RAG backend API
 */

// Get API base URL from environment variables with fallback to localhost
const getApiBaseUrl = () => {
  // In Docusaurus environment, we use process.env
  return (
    process.env.RAG_API_BASE_URL ||
    typeof window !== 'undefined'
      ? window.RAG_API_BASE_URL || 'http://localhost:8000'
      : 'http://localhost:8000'
  );
};

/**
 * Submit a query to the RAG backend
 * @param {string} query - The user's question/query
 * @param {string} sessionId - Optional session identifier for context
 * @param {object} context - Optional additional context for the query
 * @returns {Promise<object>} The response from the RAG system
 */
export const submitQuery = async (query, sessionId = null, context = null) => {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

    const response = await fetch(`${getApiBaseUrl()}/api/v1/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        session_id: sessionId,
        context: context || null,
      }),
      signal: controller.signal, // Enable cancellation
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      // Handle different error statuses
      if (response.status === 400) {
        const errorData = await response.json();
        throw new Error(`Bad Request: ${errorData.error || 'Invalid query'}`);
      } else if (response.status === 500) {
        throw new Error('Internal Server Error: The RAG service is temporarily unavailable');
      } else if (response.status === 429) {
        throw new Error('Rate Limit Exceeded: Please try again in a moment');
      } else if (response.status === 408 || response.status === 409 || response.status >= 500) {
        throw new Error(`Server Error: ${response.status} - ${response.statusText}`);
      } else {
        throw new Error(`API Error: ${response.status} - ${response.statusText}`);
      }
    }

    return await response.json();
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('Request Timeout: The request took too long to complete. Please try again.');
    } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
      throw new Error('Network Error: Unable to connect to the RAG service. Please check your connection and API configuration.');
    } else if (error.message.includes('timeout')) {
      throw new Error('Request Timeout: The request took too long to complete. Please try again.');
    }
    throw error;
  }
};

/**
 * Retry mechanism for failed API calls
 * @param {Function} apiCall - The API function to retry
 * @param {number} maxRetries - Maximum number of retry attempts
 * @param {number} delay - Initial delay in milliseconds between retries
 * @returns {Promise<any>} The result of the successful API call
 */
export const retryApiCall = async (apiCall, maxRetries = 3, delay = 1000) => {
  let lastError;

  for (let i = 0; i < maxRetries; i++) {
    try {
      return await apiCall();
    } catch (error) {
      lastError = error;

      // Don't retry on certain error types
      if (error.message.includes('Bad Request') ||
          error.message.includes('Invalid query')) {
        throw error;
      }

      // Wait before retrying (with exponential backoff)
      if (i < maxRetries - 1) {
        await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)));
      }
    }
  }

  throw lastError;
};

/**
 * Test the connection to the RAG API
 * @returns {Promise<boolean>} Whether the API is accessible
 */
export const testConnection = async () => {
  try {
    // We can't directly test the API without a query, so we'll try to make a minimal request
    // and handle the validation error appropriately
    const response = await fetch(`${getApiBaseUrl()}/api/v1/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: "", // Empty query to test connection
      }),
    });

    // If we get a validation error (400) for empty query, API is accessible
    // If we get network error, API is not accessible
    return response.status !== 404; // If endpoint doesn't exist, it's truly not accessible
  } catch (error) {
    return false;
  }
};

/**
 * Validate if the API configuration is set up correctly
 * @returns {boolean} Whether the configuration is valid
 */
export const validateConfig = () => {
  const baseUrl = getApiBaseUrl();
  return baseUrl && baseUrl.startsWith('http');
};