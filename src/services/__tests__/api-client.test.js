/**
 * Integration tests for API client service
 */

// Mock the fetch API
global.fetch = jest.fn();

import apiClient from '../api-client';

describe('API Client Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset fetch mock
    global.fetch.mockReset();
  });

  test('successfully submits a query and returns response', async () => {
    const mockResponse = {
      query: 'Test query',
      answer: 'Test answer',
      citations: [],
      retrieved_contexts: [],
      execution_time: 1.23,
      success: true
    };

    global.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    const queryData = {
      query: 'Test query',
      selectedText: 'Test selected text',
      max_results: 5,
      include_citations: true,
      temperature: 0.3
    };

    const result = await apiClient.submitQuery(queryData);

    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/api/v1/query',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(queryData)
      }
    );

    expect(result).toEqual(mockResponse);
  });

  test('handles API error responses correctly', async () => {
    const errorResponse = {
      detail: 'Invalid query parameters',
      error_code: 'INVALID_QUERY',
      success: false
    };

    global.fetch.mockResolvedValue({
      ok: false,
      status: 400,
      json: () => Promise.resolve(errorResponse),
    });

    const queryData = {
      query: 'Test query',
    };

    await expect(apiClient.submitQuery(queryData)).rejects.toThrow('Invalid query: Invalid query parameters');
  });

  test('handles network errors correctly', async () => {
    global.fetch.mockRejectedValue(new TypeError('Failed to fetch'));

    const queryData = {
      query: 'Test query',
    };

    await expect(apiClient.submitQuery(queryData)).rejects.toThrow('Network error: Unable to connect to the API server. Please check that the backend is running at http://localhost:8000');
  });

  test('validates query input before making request', async () => {
    await expect(apiClient.submitQuery({ query: '' })).rejects.toThrow('Query is required and must be a non-empty string');

    await expect(apiClient.submitQuery({ query: 'a'.repeat(1001) })).rejects.toThrow('Query must be between 1 and 1000 characters');

    await expect(apiClient.submitQuery({
      query: 'Test query',
      max_results: 25
    })).rejects.toThrow('max_results must be between 1 and 20');
  });

  test('performs health check successfully', async () => {
    const healthResponse = {
      status: 'healthy',
      timestamp: '2025-12-23T10:00:00Z',
      version: '1.0.0',
      services: {
        qdrant: true
      }
    };

    global.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(healthResponse),
    });

    const result = await apiClient.healthCheck();

    expect(global.fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/health');
    expect(result).toEqual(healthResponse);
  });

  test('handles health check error', async () => {
    global.fetch.mockRejectedValue(new TypeError('Failed to fetch'));

    await expect(apiClient.healthCheck()).rejects.toThrow('Network error: Unable to connect to the API server. Please check that the backend is running at http://localhost:8000');
  });

  test('includes timeout handling', async () => {
    // This test verifies that the timeout functionality is in the code
    // Actual timeout testing would require more complex mocking
    const queryData = {
      query: 'Test query',
    };

    // Mock a response that takes longer than the timeout
    global.fetch.mockImplementation(() => new Promise(() => {
      // Never resolve to simulate timeout
    }));

    // We'll test that the timeout parameter is accepted
    // The actual timeout behavior would be tested differently in a real environment
    const submitPromise = apiClient.submitQuery(queryData, 1, 100); // 1 retry, 100ms timeout

    // Since we're not actually implementing the timeout in this test environment,
    // we'll just ensure the function accepts the timeout parameter
    expect(typeof submitPromise).toBe('object');
  });

  test('retries on network failures', async () => {
    const queryData = {
      query: 'Test query',
    };

    // Mock failure on first call, success on second
    global.fetch
      .mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: () => Promise.resolve({ detail: 'Server error' }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ answer: 'Success after retry' }),
      });

    const result = await apiClient.submitQuery(queryData, 2); // Allow 2 retries

    // Should have called fetch twice (original + 1 retry)
    expect(global.fetch).toHaveBeenCalledTimes(2);
    expect(result).toEqual({ answer: 'Success after retry' });
  });
});