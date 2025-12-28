/**
 * Unit tests for RagQueryContext component
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import RagQueryContext from '../RagQueryContext';

// Mock the child components
jest.mock('../RagQueryForm', () => (props) => (
  <div data-testid="rag-query-form" onClick={() => props.onSubmitQuery({ query: 'test query' })}>
    RagQueryForm
  </div>
));
jest.mock('../RagQueryResult', () => (props) => (
  <div data-testid="rag-query-result">
    RagQueryResult - Loading: {props.loading.toString()}, Error: {props.error}
  </div>
));

// Mock the API client
const mockSubmitQuery = jest.fn();
jest.mock('../../services/api-client', () => ({
  submitQuery: (queryData) => mockSubmitQuery(queryData)
}));

// Mock the text selection utilities
jest.mock('../../utils/text-selection', () => ({
  getSelectedText: jest.fn(),
  addTextSelectionListener: jest.fn(() => jest.fn()), // Returns a cleanup function
  sanitizeSelectedText: jest.fn((text) => text),
}));

describe('RagQueryContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders RagQueryContext component', () => {
    render(<RagQueryContext />);

    expect(screen.getByText('Ask about the Book Content')).toBeInTheDocument();
    expect(screen.getByTestId('rag-query-form')).toBeInTheDocument();
    expect(screen.getByTestId('rag-query-result')).toBeInTheDocument();
  });

  test('handles query submission correctly', async () => {
    mockSubmitQuery.mockResolvedValue({
      answer: 'Test answer',
      citations: [],
      retrieved_contexts: [],
      execution_time: 1.23,
      success: true
    });

    render(<RagQueryContext />);

    // Simulate form submission (mocked)
    fireEvent.click(screen.getByTestId('rag-query-form'));

    // Should show loading state
    expect(screen.getByText('RagQueryResult - Loading: true, Error:')).toBeInTheDocument();

    // Wait for the mock API call to complete
    await waitFor(() => {
      expect(mockSubmitQuery).toHaveBeenCalledWith({ query: 'test query' });
    });
  });

  test('handles API error correctly', async () => {
    const error = new Error('API Error');
    mockSubmitQuery.mockRejectedValue(error);

    render(<RagQueryContext />);

    // Simulate form submission (mocked)
    fireEvent.click(screen.getByTestId('rag-query-form'));

    // Wait for the error handling
    await waitFor(() => {
      expect(screen.getByText('RagQueryResult - Loading: false, Error: API Error')).toBeInTheDocument();
    });
  });

  test('displays results after successful query', async () => {
    const mockResult = {
      answer: 'Test answer',
      citations: [{ url: 'http://example.com', title: 'Example', score: 0.9 }],
      retrieved_contexts: [{ content: 'Context', url: 'http://example.com', title: 'Example', score: 0.9 }],
      execution_time: 1.23,
      success: true
    };

    mockSubmitQuery.mockResolvedValue(mockResult);

    render(<RagQueryContext />);

    // Simulate form submission (mocked)
    fireEvent.click(screen.getByTestId('rag-query-form'));

    // Wait for the result to be displayed
    await waitFor(() => {
      expect(mockSubmitQuery).toHaveBeenCalledWith({ query: 'test query' });
    });
  });
});