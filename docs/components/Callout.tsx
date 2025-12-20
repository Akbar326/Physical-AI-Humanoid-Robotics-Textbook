import React from 'react';
import clsx from 'clsx';

type CalloutType = 'info' | 'warning' | 'danger' | 'success';

interface CalloutProps {
  type: CalloutType;
  title?: string;
  children: React.ReactNode;
}

/**
 * Callout Component
 * Provides styled callout boxes for important information
 */
const Callout: React.FC<CalloutProps> = ({ type, title, children }) => {
  const calloutClasses = clsx(
    'callout',
    `callout--${type}`,
    'margin-bottom--md',
    'padding--md',
    'border-radius--md'
  );

  const titleElement = title ? (
    <h5 className={`callout__title callout__title--${type}`}>
      {getIconForType(type)} {title}
    </h5>
  ) : null;

  return (
    <div className={calloutClasses}>
      {titleElement}
      <div className="callout__body">{children}</div>
    </div>
  );
};

/**
 * Helper function to get appropriate icon for callout type
 */
function getIconForType(type: CalloutType): string {
  switch (type) {
    case 'info':
      return 'ℹ️';
    case 'warning':
      return '⚠️';
    case 'danger':
      return '❌';
    case 'success':
      return '✅';
    default:
      return 'ℹ️';
  }
}

export default Callout;