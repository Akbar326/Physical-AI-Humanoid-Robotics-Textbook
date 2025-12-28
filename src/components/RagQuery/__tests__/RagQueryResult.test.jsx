/**
 * Unit tests for RagQueryResult component
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import RagQueryResult from '../RagQueryResult';

describe('RagQueryResult', () => {
  test('renders empty state when no result is provided', () => {
    render(<RagQueryResult result={null} loading={false} error={''} />);

    expect(screen.getByText('Submit a query to see results here.')).toBeInTheDocument();
  });

  test('renders loading state', () => {
    render(<RagQueryResult result={null} loading={true} error={''} />);

    expect(screen.getByText('Processing your query...')).toBeInTheDocument();
  });

  test('renders error state', () => {
    render(<RagQueryResult result={null} loading={false} error="Test error" />);

    expect(screen.getByText('Error')).toBeInTheDocument();
    expect(screen.getByText('Test error')).toBeInTheDocument();
  });

  test('renders query result correctly', () => {
    const mockResult = {
      answer: 'This is the answer to your query',
      citations: [
        { url: 'http://example.com', title: 'Example Citation', score: 0.9 }
      ],
      retrieved_contexts: [
        { content: 'This is the retrieved context', url: 'http://example.com', title: 'Example Context', score: 0.9 }
      ],
      execution_time: 1.23
    };

    render(<RagQueryResult result={mockResult} loading={false} error={''} />);

    expect(screen.getByText('This is the answer to your query')).toBeInTheDocument();
    expect(screen.getByText('Answer')).toBeInTheDocument();
    expect(screen.getByText('Sources')).toBeInTheDocument();
    expect(screen.getByText('Retrieved Context')).toBeInTheDocument();
    expect(screen.getByText('Response time: 1.23 seconds')).toBeInTheDocument();
  });

  test('renders multiple citations', () => {
    const mockResult = {
      answer: 'Test answer',
      citations: [
        { url: 'http://example1.com', title: 'Example Citation 1', score: 0.9 },
        { url: 'http://example2.com', title: 'Example Citation 2', score: 0.8 }
      ]
    };

    render(<RagQueryResult result={mockResult} loading={false} error={''} />);

    expect(screen.getByText('Example Citation 1')).toBeInTheDocument();
    expect(screen.getByText('Example Citation 2')).toBeInTheDocument();
  });

  test('renders multiple contexts', () => {
    const mockResult = {
      answer: 'Test answer',
      retrieved_contexts: [
        { content: 'Context 1', url: 'http://example1.com', title: 'Context 1 Title', score: 0.9 },
        { content: 'Context 2', url: 'http://example2.com', title: 'Context 2 Title', score: 0.8 }
      ]
    };

    render(<RagQueryResult result={mockResult} loading={false} error={''} />);

    expect(screen.getByText('Context 1 Title')).toBeInTheDocument();
    expect(screen.getByText('Context 2 Title')).toBeInTheDocument();
  });

  test('handles result with no citations or contexts', () => {
    const mockResult = {
      answer: 'Test answer',
      execution_time: 0.5
    };

    render(<RagQueryResult result={mockResult} loading={false} error={''} />);

    expect(screen.getByText('Test answer')).toBeInTheDocument();
    expect(screen.getByText('Response time: 0.50 seconds')).toBeInTheDocument();
    // Citations and contexts sections should not be present
    expect(screen.queryByText('Sources')).not.toBeInTheDocument();
    expect(screen.queryByText('Retrieved Context')).not.toBeInTheDocument();
  });
});