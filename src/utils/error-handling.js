/**
 * Error Handling Utilities
 *
 * This utility provides functions for handling and formatting errors
 * in the frontend-backend integration.
 */

/**
 * Format error messages for display to users
 * @param {Error|string} error - The error to format
 * @param {string} fallbackMessage - Fallback message if error formatting fails
 * @returns {string} Formatted error message
 */
export function formatErrorMessage(error, fallbackMessage = 'An error occurred') {
  if (!error) {
    return fallbackMessage;
  }

  // If it's already a string, return it
  if (typeof error === 'string') {
    return error;
  }

  // If it's an error object, try to extract the message
  if (error instanceof Error) {
    return error.message || fallbackMessage;
  }

  // If it's an object with a message property
  if (error.message) {
    return error.message;
  }

  // If it's an object that might contain API error details
  if (typeof error === 'object') {
    // Check for common API error response formats
    if (error.detail) {
      return error.detail;
    }
    if (error.error) {
      return error.error;
    }
    if (error.message) {
      return error.message;
    }
  }

  // As a last resort, try to convert to string
  try {
    return String(error) || fallbackMessage;
  } catch {
    return fallbackMessage;
  }
}

/**
 * Check if an error is a network error
 * @param {Error} error - The error to check
 * @returns {boolean} True if it's a network error, false otherwise
 */
export function isNetworkError(error) {
  if (!error) {
    return false;
  }

  // Check if it's a network-related error
  if (error.message && (
    error.message.includes('NetworkError') ||
    error.message.includes('Failed to fetch') ||
    error.message.includes('Network Error') ||
    error.message.includes('fetch') ||
    error.message.includes('CORS') ||
    error.message.includes('cross-origin')
  )) {
    return true;
  }

  // Check for common HTTP error status codes that indicate network issues
  if (error.status) {
    const networkErrorCodes = [0, 502, 503, 504]; // 0 often indicates network issues
    return networkErrorCodes.includes(error.status);
  }

  return false;
}

/**
 * Check if an error is a client-side validation error
 * @param {Error} error - The error to check
 * @returns {boolean} True if it's a validation error, false otherwise
 */
export function isValidationError(error) {
  if (!error || !error.message) {
    return false;
  }

  // Check if the error message indicates validation issues
  const validationKeywords = [
    'validation',
    'invalid',
    'required',
    'must be',
    'should be',
    'exceeds',
    'minimum',
    'maximum',
    'format'
  ];

  const lowerMessage = error.message.toLowerCase();
  return validationKeywords.some(keyword => lowerMessage.includes(keyword));
}

/**
 * Log error with additional context
 * @param {Error} error - The error to log
 * @param {string} context - Context information about where the error occurred
 * @param {Object} additionalData - Additional data to log with the error
 */
export function logError(error, context = '', additionalData = {}) {
  const errorLog = {
    timestamp: new Date().toISOString(),
    context,
    message: formatErrorMessage(error),
    isNetworkError: isNetworkError(error),
    isValidationError: isValidationError(error),
    additionalData
  };

  // Add error object properties if available
  if (error && typeof error === 'object') {
    errorLog.errorName = error.name;
    errorLog.errorStack = error.stack;
    if (error.status) errorLog.status = error.status;
    if (error.url) errorLog.url = error.url;
  }

  console.error('Error Log:', errorLog);
}

/**
 * Create a user-friendly error message based on error type
 * @param {Error} error - The error to create a message for
 * @returns {string} User-friendly error message
 */
export function createUserFriendlyErrorMessage(error) {
  if (isNetworkError(error)) {
    return 'Unable to connect to the service. Please check your connection and try again.';
  }

  if (isValidationError(error)) {
    return formatErrorMessage(error);
  }

  // Handle specific error codes if available
  if (error && typeof error === 'object') {
    switch (error.error_code) {
      case 'INVALID_QUERY':
        return 'Your query is invalid. Please make sure it contains between 1 and 1000 characters.';
      case 'RATE_LIMIT_EXCEEDED':
        return 'Too many requests. Please wait a moment before trying again.';
      case 'RETRIEVAL_ERROR':
        return 'Unable to retrieve relevant information. Please try a different query.';
      case 'AGENT_ERROR':
        return 'The AI service is temporarily unavailable. Please try again later.';
      default:
        break;
    }
  }

  // Default fallback
  return 'An error occurred while processing your request. Please try again.';
}

/**
 * Error boundary component for React components
 * This is a higher-order component that catches JavaScript errors anywhere in the child component tree
 */
export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log the error to an error reporting service
    logError(error, 'ErrorBoundary', { errorInfo });
  }

  render() {
    if (this.state.hasError) {
      // You can render any custom fallback UI
      return (
        <div className="error-boundary">
          <h2>Something went wrong.</h2>
          <p>{createUserFriendlyErrorMessage(this.state.error)}</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}