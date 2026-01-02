import React from 'react';
import GlobalChat from '../components/GlobalChat/GlobalChat';

// Default implementation, that you can customize
function Root({ children }) {
  return (
    <React.Fragment>
      {children}
      <GlobalChat />
    </React.Fragment>
  );
}

export default Root;