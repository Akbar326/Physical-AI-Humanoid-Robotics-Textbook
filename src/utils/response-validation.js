/**
 * Response Validation Utilities
 *
 * This utility provides functions for validating API responses
 * to ensure quality and proper format.
 */

/**
 * Validates the structure and content of an API response
 * @param {any} response - The API response to validate
 * @returns {Object} Validation result with isValid boolean and optional error message
 */
export function validateApiResponse(response) {
  if (!response || typeof response !== 'object') {
    return {
      isValid: false,
      error: 'Response must be an object'
    };
  }

  // Check required fields
  const requiredFields = ['query', 'answer', 'success'];
  for (const field of requiredFields) {
    if (!(field in response)) {
      return {
        isValid: false,
        error: `Response is missing required field: ${field}`
      };
    }
  }

  // Validate field types
  if (typeof response.query !== 'string') {
    return {
      isValid: false,
      error: 'Response query must be a string'
    };
  }

  if (typeof response.answer !== 'string') {
    return {
      isValid: false,
      error: 'Response answer must be a string'
    };
  }

  if (typeof response.success !== 'boolean') {
    return {
      isValid: false,
      error: 'Response success must be a boolean'
    };
  }

  // Validate optional arrays if they exist
  if (response.citations !== undefined) {
    if (!Array.isArray(response.citations)) {
      return {
        isValid: false,
        error: 'Response citations must be an array'
      };
    }

    // Validate citation structure if array is not empty
    if (response.citations.length > 0) {
      for (let i = 0; i < response.citations.length; i++) {
        const citation = response.citations[i];
        if (!citation || typeof citation !== 'object') {
          return {
            isValid: false,
            error: `Citation at index ${i} must be an object`
          };
        }

        if (!citation.url || typeof citation.url !== 'string') {
          return {
            isValid: false,
            error: `Citation at index ${i} must have a valid url string`
          };
        }

        if (!citation.title || typeof citation.title !== 'string') {
          return {
            isValid: false,
            error: `Citation at index ${i} must have a valid title string`
          };
        }

        if (citation.score !== undefined && typeof citation.score !== 'number') {
          return {
            isValid: false,
            error: `Citation at index ${i} score must be a number`
          };
        }
      }
    }
  }

  if (response.retrieved_contexts !== undefined) {
    if (!Array.isArray(response.retrieved_contexts)) {
      return {
        isValid: false,
        error: 'Response retrieved_contexts must be an array'
      };
    }

    // Validate context structure if array is not empty
    if (response.retrieved_contexts.length > 0) {
      for (let i = 0; i < response.retrieved_contexts.length; i++) {
        const context = response.retrieved_contexts[i];
        if (!context || typeof context !== 'object') {
          return {
            isValid: false,
            error: `Retrieved context at index ${i} must be an object`
          };
        }

        if (!context.content || typeof context.content !== 'string') {
          return {
            isValid: false,
            error: `Retrieved context at index ${i} must have a valid content string`
          };
        }

        if (!context.url || typeof context.url !== 'string') {
          return {
            isValid: false,
            error: `Retrieved context at index ${i} must have a valid url string`
          };
        }

        if (!context.title || typeof context.title !== 'string') {
          return {
            isValid: false,
            error: `Retrieved context at index ${i} must have a valid title string`
          };
        }

        if (context.score !== undefined && typeof context.score !== 'number') {
          return {
            isValid: false,
            error: `Retrieved context at index ${i} score must be a number`
          };
        }
      }
    }
  }

  // Validate execution time if present
  if (response.execution_time !== undefined && typeof response.execution_time !== 'number') {
    return {
      isValid: false,
      error: 'Response execution_time must be a number'
    };
  }

  return {
    isValid: true
  };
}

/**
 * Checks if a response contains meaningful content
 * @param {Object} response - The API response to check
 * @returns {Object} Quality check result with isQuality boolean and optional feedback
 */
export function checkResponseQuality(response) {
  const validation = validateApiResponse(response);
  if (!validation.isValid) {
    return {
      isQuality: false,
      feedback: validation.error
    };
  }

  // Check if answer is substantial
  if (!response.answer || response.answer.trim().length < 10) {
    return {
      isQuality: false,
      feedback: 'Response answer is too short'
    };
  }

  // Check if answer appears to be a proper response
  const answer = response.answer.trim();
  if (answer.toLowerCase().includes('i don\'t know') ||
      answer.toLowerCase().includes('i cannot') ||
      answer.toLowerCase().includes('no information')) {
    return {
      isQuality: false,
      feedback: 'Response indicates lack of knowledge or information'
    };
  }

  // Check if citations are provided when expected
  if (response.include_citations && (!response.citations || response.citations.length === 0)) {
    return {
      isQuality: false,
      feedback: 'No citations provided when citations were requested'
    };
  }

  return {
    isQuality: true
  };
}

/**
 * Sanitizes a response by removing potentially harmful content
 * @param {Object} response - The API response to sanitize
 * @returns {Object} Sanitized response
 */
export function sanitizeResponse(response) {
  if (!response || typeof response !== 'object') {
    return null;
  }

  // Create a new object to avoid modifying the original
  const sanitized = { ...response };

  // Sanitize answer
  if (typeof response.answer === 'string') {
    sanitized.answer = response.answer.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
  }

  // Sanitize citations
  if (Array.isArray(response.citations)) {
    sanitized.citations = response.citations.map(citation => {
      if (!citation || typeof citation !== 'object') return citation;

      return {
        ...citation,
        title: typeof citation.title === 'string' ? citation.title.replace(/<[^>]*>/g, '') : citation.title,
        url: typeof citation.url === 'string' ? citation.url.replace(/[^a-zA-Z0-9\-_.~:/?#\[\]@!$&'()*+,;=%]/g, encodeURIComponent) : citation.url
      };
    });
  }

  // Sanitize retrieved contexts
  if (Array.isArray(response.retrieved_contexts)) {
    sanitized.retrieved_contexts = response.retrieved_contexts.map(context => {
      if (!context || typeof context !== 'object') return context;

      return {
        ...context,
        title: typeof context.title === 'string' ? context.title.replace(/<[^>]*>/g, '') : context.title,
        content: typeof context.content === 'string' ? context.content.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '') : context.content,
        url: typeof context.url === 'string' ? context.url.replace(/[^a-zA-Z0-9\-_.~:/?#\[\]@!$&'()*+,;=%]/g, encodeURIComponent) : context.url
      };
    });
  }

  return sanitized;
}