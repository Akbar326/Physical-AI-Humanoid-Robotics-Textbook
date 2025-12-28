# API Integration Process Documentation

This document details the process and implementation of the frontend-backend API integration for the RAG query system.

## Overview

The API integration connects the Docusaurus-based frontend textbook to a FastAPI backend that provides RAG (Retrieval-Augmented Generation) capabilities. Users can submit natural language queries about book content and receive AI-generated responses grounded in the retrieved context.

## Architecture

```
Frontend (Docusaurus/React) ←→ HTTP/REST API ←→ Backend (FastAPI)
     ↓                              ↓                  ↓
- RagQuery Components        - /api/v1/query      - RAG Agent
- API Client Service         - /api/v1/health     - Vector DB (Qdrant)
- Text Selection Utils                          - LLM Integration
- Error Handling Utils
```

## API Endpoints

### Query Endpoint
- **URL**: `POST /api/v1/query`
- **Description**: Submit a natural language query to the RAG agent
- **Request Body**:
  ```json
  {
    "query": "What are the key concepts in AI robotics?",
    "selectedText": "Optional text selected by user for context",
    "max_results": 5,
    "include_citations": true,
    "temperature": 0.3
  }
  ```
- **Response**:
  ```json
  {
    "query": "What are the key concepts in AI robotics?",
    "answer": "AI robotics combines artificial intelligence with robotics...",
    "citations": [...],
    "retrieved_contexts": [...],
    "execution_time": 2.34,
    "success": true
  }
  ```

### Health Check Endpoint
- **URL**: `GET /api/v1/health`
- **Description**: Check the health status of the API service
- **Response**:
  ```json
  {
    "status": "healthy",
    "timestamp": "2025-12-23T10:00:00Z",
    "version": "1.0.0",
    "services": {
      "qdrant": true
    }
  }
  ```

## Frontend Implementation

### API Client Service
The `api-client.js` service handles all communication with the backend:

- **Base URL**: Configurable (default: `http://localhost:8000`)
- **Timeout**: 30 seconds with configurable option
- **Retry Logic**: Exponential backoff with 2 retries by default
- **Error Handling**: Comprehensive error categorization and user-friendly messages
- **Input Validation**: Client-side validation before making requests

### Components
- **RagQueryContext**: Main orchestrator component
- **RagQueryForm**: Handles user input and text selection
- **RagQueryResult**: Displays API responses with citations
- **LoadingIndicator**: Visual feedback during API requests

### Text Selection
The system captures selected text using browser APIs:
- `window.getSelection()` for cross-browser compatibility
- Automatic inclusion of selected text in query context
- Sanitization and validation of selected text

## Error Handling

### Network Errors
- Connection failures show user-friendly messages
- Automatic retry logic for transient network issues
- Graceful degradation when backend is unavailable

### Validation Errors
- Client-side validation of query parameters
- Server-side validation with detailed error messages
- Proper error categorization (4xx vs 5xx)

### Timeout Handling
- Configurable timeout (default 30 seconds)
- User feedback during long-running requests
- Proper error handling for timeout scenarios

## Security Considerations

### Input Sanitization
- Query input validation (1-1000 characters)
- Selected text sanitization
- HTML sanitization in responses

### Error Messages
- Avoid exposing system details in error messages
- User-friendly error descriptions
- Proper error categorization

## Performance Optimization

### Loading States
- Visual feedback during API requests
- Disabled form during submission
- Clear indication of processing state

### Response Validation
- Structure validation of API responses
- Quality checks on response content
- Sanitization of response data

## Testing Strategy

### Unit Tests
- Component-level tests for React components
- Service-level tests for API client
- Utility function tests

### Integration Tests
- API client integration with mock fetch
- End-to-end workflow validation
- Error handling verification

### End-to-End Tests
- Complete user journey validation
- Cross-user story functionality checks
- Performance and error scenario testing

## Deployment Considerations

### CORS Configuration
- Backend configured for local development (localhost:3000)
- Production CORS settings as needed

### Environment Configuration
- Configurable API base URL
- Timeout and retry settings
- Development vs production settings

## Usage Examples

### Basic Query
```javascript
import apiClient from './services/api-client';

const result = await apiClient.submitQuery({
  query: "Explain reinforcement learning in robotics",
  max_results: 5,
  include_citations: true
});
```

### Context-Aware Query
```javascript
const result = await apiClient.submitQuery({
  query: "How does this apply to navigation?",
  selectedText: "Path planning algorithms determine the optimal route...",
  temperature: 0.5
});
```

## Troubleshooting

### Common Issues
- **Backend Not Running**: Ensure backend server is accessible at configured URL
- **CORS Errors**: Verify backend CORS settings
- **Timeout Errors**: Check network connectivity and backend performance
- **Validation Errors**: Ensure query parameters meet requirements

### Debugging
- Enable browser developer tools to inspect API requests
- Check browser console for JavaScript errors
- Monitor backend logs for API request handling
- Use network tab to analyze request/response details