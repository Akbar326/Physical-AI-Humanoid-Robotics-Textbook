import React from 'react';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

type OSTab = 'Ubuntu' | 'Windows' | 'macOS';
type DifficultyTab = 'Beginner' | 'Intermediate' | 'Advanced';

interface OSTabsProps {
  children: React.ReactNode[];
  defaultValue?: OSTab;
}

interface DifficultyTabsProps {
  children: React.ReactNode[];
  defaultValue?: DifficultyTab;
}

interface AlternativeTabsProps {
  labels: string[];
  children: React.ReactNode[];
}

/**
 * OS-Specific Tabs Component
 * Provides tabs for Ubuntu, Windows, and macOS instructions
 */
export const OSTabs: React.FC<OSTabsProps> = ({ children, defaultValue = 'Ubuntu' }) => {
  return (
    <Tabs
      groupId="operating-system"
      defaultValue={defaultValue}
      values={[
        { label: 'Ubuntu', value: 'Ubuntu' },
        { label: 'Windows', value: 'Windows' },
        { label: 'macOS', value: 'macOS' },
      ]}>
      {children}
    </Tabs>
  );
};

/**
 * Difficulty Level Tabs Component
 * Provides tabs for different difficulty levels
 */
export const DifficultyTabs: React.FC<DifficultyTabsProps> = ({ children, defaultValue = 'Beginner' }) => {
  return (
    <Tabs
      groupId="difficulty-level"
      defaultValue={defaultValue}
      values={[
        { label: 'Beginner', value: 'Beginner' },
        { label: 'Intermediate', value: 'Intermediate' },
        { label: 'Advanced', value: 'Advanced' },
      ]}>
      {children}
    </Tabs>
  );
};

/**
 * Alternative Approaches Tabs Component
 * Provides tabs for different implementation approaches
 */
export const AlternativeTabs: React.FC<AlternativeTabsProps> = ({ labels, children }) => {
  const values = labels.map((label, index) => ({
    label: label,
    value: `tab-${index}`,
  }));

  return (
    <Tabs groupId="alternative-approaches" values={values}>
      {children}
    </Tabs>
  );
};

export default OSTabs;