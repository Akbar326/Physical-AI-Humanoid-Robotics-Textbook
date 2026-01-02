import React from 'react';
import SafeGlobalChat from '../components/GlobalChat/SafeGlobalChat';
import ErrorBoundary from '../components/GlobalChat/ErrorBoundary';

// Default implementation, that you can customize
function Root({ children }) {
  return (
    <React.Fragment>
      {children}
      <ErrorBoundary>
        <SafeGlobalChat />
      </ErrorBoundary>
    </React.Fragment>
  );
}

export default Root;