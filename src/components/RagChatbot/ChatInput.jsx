import React, { useState } from 'react';
import styles from './RagChatbot.module.css';

/**
 * Component for chat input field and send button
 * Handles user input and submission of queries
 */
const ChatInput = ({ onQuerySubmit, disabled = false }) => {
  const [inputValue, setInputValue] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmedInput = inputValue.trim();

    // Input validation
    if (!trimmedInput) return; // Empty input

    if (trimmedInput.length > 1000) {
      setError('Query is too long. Please keep your query under 1000 characters.');
      return;
    }

    setError(''); // Clear any previous errors
    if (!disabled) {
      onQuerySubmit(trimmedInput);
      setInputValue('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.chatInputForm}>
      <div className={styles.inputContainer}>
        <textarea
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            // Clear error when user starts typing again
            if (error && e.target.value.length <= 1000) {
              setError('');
            }
          }}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about the AI-Humanoid-Robotics textbook..."
          className={`${styles.chatInput} ${error ? styles.inputError : ''}`}
          disabled={disabled}
          rows="1"
          aria-label="Chat input"
          maxLength="1000"
        />
        <button
          type="submit"
          disabled={disabled || !inputValue.trim() || error !== ''}
          className={`${styles.sendButton} ${disabled ? styles.sendButtonDisabled : ''}`}
          aria-label="Send message"
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={styles.sendIcon}
          >
            <path
              d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </button>
      </div>
      {error && (
        <div className={styles.inputErrorMessage}>
          {error}
        </div>
      )}
    </form>
  );
};

export default ChatInput;