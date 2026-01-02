/**
 * Text Selection Utility
 *
 * This utility provides functions for capturing selected text in the document
 * and managing text selection functionality for context-aware queries.
 */

/**
 * Get the currently selected text in the document
 * @returns {string} The selected text, or empty string if no text is selected
 */
export function getSelectedText() {
  const selection = window.getSelection ? window.getSelection() : document.selection;
  if (selection) {
    return selection.toString().trim();
  }
  return '';
}

/**
 * Get detailed information about the current text selection
 * @returns {Object|null} Object containing selection details, or null if no selection
 */
export function getSelectedTextInfo() {
  const selection = window.getSelection ? window.getSelection() : document.selection;

  if (!selection || selection.toString().trim() === '') {
    return null;
  }

  const range = selection.rangeCount > 0 ? selection.getRangeAt(0) : null;

  if (!range) {
    return null;
  }

  return {
    text: selection.toString().trim(),
    range: range,
    startContainer: range.startContainer,
    startOffset: range.startOffset,
    endContainer: range.endContainer,
    endOffset: range.endOffset,
    rect: range.getBoundingClientRect()
  };
}

/**
 * Check if there is currently selected text
 * @returns {boolean} True if text is selected, false otherwise
 */
export function hasSelectedText() {
  return getSelectedText().length > 0;
}

/**
 * Clear the current text selection
 */
export function clearSelection() {
  if (window.getSelection) {
    window.getSelection().removeAllRanges();
  } else if (document.selection) {
    document.selection.empty();
  }
}

/**
 * Add an event listener for text selection changes
 * @param {Function} callback - Function to call when text selection changes
 * @returns {Function} Function to remove the event listener
 */
export function addTextSelectionListener(callback) {
  const handleSelectionChange = () => {
    callback(getSelectedTextInfo());
  };

  document.addEventListener('selectionchange', handleSelectionChange);

  // Return a function to remove the event listener
  return () => {
    document.removeEventListener('selectionchange', handleSelectionChange);
  };
}

/**
 * Validate selected text for API submission
 * @param {string} text - The selected text to validate
 * @returns {Object} Validation result with isValid boolean and optional error message
 */
export function validateSelectedText(text) {
  if (typeof text !== 'string') {
    return {
      isValid: false,
      error: 'Selected text must be a string'
    };
  }

  if (text.length === 0) {
    return {
      isValid: false,
      error: 'Selected text cannot be empty'
    };
  }

  if (text.length > 5000) { // Reasonable limit for context
    return {
      isValid: false,
      error: 'Selected text is too long (maximum 5000 characters)'
    };
  }

  return {
    isValid: true
  };
}

/**
 * Sanitize selected text before sending to API
 * @param {string} text - The selected text to sanitize
 * @returns {string} Sanitized text
 */
export function sanitizeSelectedText(text) {
  if (typeof text !== 'string') {
    return '';
  }

  // Remove extra whitespace while preserving single spaces
  return text.replace(/\s+/g, ' ').trim();
}