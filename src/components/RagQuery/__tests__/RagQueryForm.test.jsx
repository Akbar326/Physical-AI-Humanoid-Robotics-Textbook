/**
 * Unit tests for RagQueryForm component
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import RagQueryForm from '../RagQueryForm';

// Mock the text selection utilities
jest.mock('../../utils/text-selection', () => ({
  getSelectedText: jest.fn(),
  addTextSelectionListener: jest.fn(() => jest.fn()), // Returns a cleanup function
  sanitizeSelectedText: jest.fn((text) => text),
}));

describe('RagQueryForm', () => {
  const mockOnSubmitQuery = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders query form correctly', () => {
    render(<RagQueryForm onSubmitQuery={mockOnSubmitQuery} />);

    expect(screen.getByPlaceholderText('Ask a question about the book content...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit query/i })).toBeInTheDocument();
  });

  test('allows user to enter a query', () => {
    render(<RagQueryForm onSubmitQuery={mockOnSubmitQuery} />);

    const queryInput = screen.getByPlaceholderText('Ask a question about the book content...');
    fireEvent.change(queryInput, { target: { value: 'Test query' } });

    expect(queryInput.value).toBe('Test query');
  });

  test('submits query when submit button is clicked', async () => {
    render(<RagQueryForm onSubmitQuery={mockOnSubmitQuery} />);

    const queryInput = screen.getByPlaceholderText('Ask a question about the book content...');
    fireEvent.change(queryInput, { target: { value: 'Test query' } });

    const submitButton = screen.getByRole('button', { name: /submit query/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmitQuery).toHaveBeenCalledWith({
        query: 'Test query',
        selectedText: null,
      });
    });
  });

  test('shows error when query is empty', async () => {
    render(<RagQueryForm onSubmitQuery={mockOnSubmitQuery} />);

    const submitButton = screen.getByRole('button', { name: /submit query/i });
    fireEvent.click(submitButton);

    expect(await screen.findByText('Please enter a query')).toBeInTheDocument();
  });

  test('disables submit button when query is empty', () => {
    render(<RagQueryForm onSubmitQuery={mockOnSubmitQuery} />);

    const submitButton = screen.getByRole('button', { name: /submit query/i });
    expect(submitButton).toBeDisabled();
  });

  test('enables submit button when query is entered', () => {
    render(<RagQueryForm onSubmitQuery={mockOnSubmitQuery} />);

    const queryInput = screen.getByPlaceholderText('Ask a question about the book content...');
    fireEvent.change(queryInput, { target: { value: 'Test query' } });

    const submitButton = screen.getByRole('button', { name: /submit query/i });
    expect(submitButton).not.toBeDisabled();
  });

  test('shows submitting state during query submission', async () => {
    // Mock a promise that takes some time to resolve
    const mockPromise = new Promise((resolve) => {
      setTimeout(() => resolve({ answer: 'Test answer' }), 100);
    });
    mockOnSubmitQuery.mockReturnValue(mockPromise);

    render(<RagQueryForm onSubmitQuery={mockOnSubmitQuery} />);

    const queryInput = screen.getByPlaceholderText('Ask a question about the book content...');
    fireEvent.change(queryInput, { target: { value: 'Test query' } });

    const submitButton = screen.getByRole('button', { name: /submit query/i });
    fireEvent.click(submitButton);

    // Button should show "Submitting..." text
    expect(submitButton).toHaveTextContent('Submitting...');
    expect(submitButton).toBeDisabled();
  });
});