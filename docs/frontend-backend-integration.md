# Frontend-Backend Integration Documentation

This document provides comprehensive information about the integration between the frontend Docusaurus application and the RAG backend API.

## Overview

The frontend-backend integration enables users to submit natural language queries about book content directly from the book UI. The system supports both basic queries and context-aware queries using selected text. The integration follows a client-server architecture where the frontend makes API calls to the FastAPI backend.

## Components

### RagQueryContext
The main component that provides context and state management for the RAG query system. It manages communication between form and result components, handles API calls, and manages loading/error states.

### RagQueryForm
A form component that allows users to submit queries about book content. It integrates with text selection utilities to enable context-aware queries with selected text.

### RagQueryResult
A component that displays the results from the RAG query API, including the answer, citations, and retrieved contexts.

### LoadingIndicator
A reusable loading indicator component for API requests.

### API Client Service
A service that handles communication with the backend RAG API, providing methods for submitting queries and handling responses.

### Text Selection Utility
A utility that provides functions for capturing selected text in the document and managing text selection functionality.

### Error Handling Utilities
Utilities that provide functions for handling and formatting errors in the frontend-backend integration.

## API Integration

### Endpoints
- `POST /api/v1/query` - Submit a query to the RAG backend
- `GET /api/v1/health` - Check the health status of the API service

### Query Format
The query endpoint expects a JSON object with the following properties:
- `query` (string, required): The natural language query from the user (1-1000 characters)
- `selectedText` (string, optional): Text selected by the user for context-aware queries
- `max_results` (integer, optional): Maximum number of context results to retrieve (1-20, default: 5)
- `include_citations` (boolean, optional): Whether to include source citations in response (default: true)
- `temperature` (number, optional): Controls response creativity (0.0-1.0, default: 0.3)

### Response Format
The API returns a JSON object with:
- `query` (string): Echo of the original query
- `answer` (string): The agent's response grounded in retrieved context
- `citations` (array): Sources used in the response
- `retrieved_contexts` (array): Full context snippets retrieved
- `execution_time` (number): Time taken to process the request in seconds
- `success` (boolean): Whether the request was processed successfully

## Usage

### Adding to a Page
To add the query functionality to a Docusaurus page, import and use the RagQueryContext component:

```jsx
import RagQueryContext from './components/RagQuery/RagQueryContext';

function MyBookPage() {
  return (
    <div>
      <h1>My Book Page</h1>
      <p>Page content here...</p>
      <RagQueryContext />
    </div>
  );
}
```

### Text Selection
The system automatically detects text selection on the page. When text is selected, it appears as context in the query form. Users can then ask questions specifically about the selected text.

## Error Handling

The system includes comprehensive error handling:
- Network error detection with user-friendly messages
- Timeout handling with configurable timeout (default 30 seconds)
- Retry logic with exponential backoff (default 2 retries)
- Proper error categorization (client vs server errors)
- Validation error handling for bad requests
- Graceful degradation when API is unavailable

## Configuration

The API client is configured to connect to `http://localhost:8000` by default. This can be changed by passing a different base URL to the API client constructor.

## Performance Considerations

- Loading indicators are shown during API requests
- Response validation ensures quality
- Proper error handling prevents crashes
- Efficient state management avoids unnecessary re-renders

## Security

- Input sanitization is performed on selected text
- Proper validation of query parameters
- Error messages don't expose system details
- CORS is configured for local development

## Development

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   python run_server.py
   ```

2. Start the frontend:
   ```bash
   npm run start
   ```

The backend should be available at `http://localhost:8000` and the frontend at `http://localhost:3000`.

### Testing

The system includes test files for:
- Query submission functionality
- Context-aware queries
- Error handling scenarios
- API integration

Run tests using the appropriate test runner for your environment.