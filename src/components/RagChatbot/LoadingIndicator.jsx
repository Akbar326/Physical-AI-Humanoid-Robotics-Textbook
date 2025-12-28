import React from 'react';
import styles from './RagChatbot.module.css';

/**
 * Component to display loading state while waiting for API responses
 */
const LoadingIndicator = () => {
  return (
    <div className={styles.loadingContainer}>
      <div className={styles.loadingMessage}>
        <div className={styles.loadingDots}>
          <span className={styles.dot}></span>
          <span className={styles.dot}></span>
          <span className={styles.dot}></span>
        </div>
        <p>Thinking...</p>
      </div>
    </div>
  );
};

export default LoadingIndicator;