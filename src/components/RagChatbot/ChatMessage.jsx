import React from 'react';
import styles from './RagChatbot.module.css';

/**
 * Component to display individual messages in the chat
 * Handles different message types (user, assistant, system) with appropriate styling
 */
const ChatMessage = ({ message, sender, timestamp, sources, isError = false }) => {
  // Format timestamp for display
  const formatTime = (date) => {
    if (!date) return '';
    return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Determine CSS classes based on sender and error state
  const getMessageClass = () => {
    let baseClass = styles.message;

    switch (sender) {
      case 'user':
        return `${baseClass} ${styles.userMessage}`;
      case 'assistant':
        return `${baseClass} ${styles.assistantMessage}`;
      case 'system':
        return `${baseClass} ${styles.systemMessage} ${isError ? styles.errorMessage : ''}`;
      default:
        return baseClass;
    }
  };

  // Render sources if available (for assistant messages)
  const renderSources = () => {
    if (!sources || sources.length === 0) {
      return null;
    }

    return (
      <div className={styles.sources}>
        <h4 className={styles.sourcesTitle}>Sources:</h4>
        <ul className={styles.sourcesList}>
          {sources.map((source, index) => (
            <li key={index} className={styles.sourceItem}>
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.sourceLink}
              >
                {source.title || 'Source'}
              </a>
              <p className={styles.sourceContent}>{source.content}</p>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  return (
    <div className={getMessageClass()} role="listitem">
      <div className={styles.messageContent}>
        <div className={styles.messageText} aria-label={`${sender} message: ${message}`}>
          {message}
        </div>
        {sender === 'assistant' && renderSources()}
      </div>
      {timestamp && (
        <div className={styles.messageTimestamp} aria-label={`Sent at ${formatTime(timestamp)}`}>
          {formatTime(timestamp)}
        </div>
      )}
    </div>
  );
};

export default ChatMessage;