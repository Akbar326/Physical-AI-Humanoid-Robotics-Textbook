/**
 * LoadingIndicator Component
 *
 * A reusable loading indicator component for API requests.
 */

import React from 'react';

const LoadingIndicator = ({ message = 'Loading...', size = 'medium' }) => {
  const sizeClasses = {
    small: 'loading-spinner-small',
    medium: 'loading-spinner-medium',
    large: 'loading-spinner-large'
  };

  const sizeClass = sizeClasses[size] || sizeClasses.medium;

  return (
    <div className="loading-indicator-container">
      <div className={`loading-spinner ${sizeClass}`}></div>
      {message && <p className="loading-message">{message}</p>}

      <style jsx>{`
        .loading-indicator-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }

        .loading-spinner {
          border: 3px solid #f3f3f3;
          border-top: 3px solid #2196f3;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        .loading-spinner-small {
          width: 20px;
          height: 20px;
        }

        .loading-spinner-medium {
          width: 40px;
          height: 40px;
        }

        .loading-spinner-large {
          width: 60px;
          height: 60px;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .loading-message {
          margin-top: 10px;
          color: #666;
          font-size: 14px;
        }
      `}</style>
    </div>
  );
};

export default LoadingIndicator;