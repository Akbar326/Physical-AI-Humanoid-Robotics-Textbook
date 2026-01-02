# API Contract: RAG Chatbot Integration

## Overview

This document defines the API contract between the Docusaurus frontend chatbot component and the FastAPI RAG backend.

## Base URL

The API base URL is configurable via environment variables:
- Development: `http://localhost:8000`
- Production: Configured via `RAG_API_BASE_URL` environment variable

## Endpoints

### POST /api/v1/query

Submit a user query to the RAG system and receive an AI-generated response.

#### Request

**Headers**:
- `Content-Type: application/json`
- `Accept: application/json`

**Body**:
```json
{
  "query": "string (required) - The user's question/query",
  "session_id": "string (optional) - Session identifier for context",
  "context": "object (optional) - Additional context for the query"
}
```

#### Response

**Success Response (200 OK)**:
```json
{
  "response": "string - The AI-generated response to the query",
  "sources": [
    {
      "title": "string - Title of the source document",
      "url": "string - URL to the source document",
      "content": "string - Relevant excerpt from the source",
      "score": "number - Relevance score of the source"
    }
  ],
  "session_id": "string - Session identifier (if provided in request)",
  "timestamp": "string - ISO 8601 timestamp of the response"
}
```

**Error Response (400 Bad Request)**:
```json
{
  "error": "string - Error message describing the issue",
  "code": "string - Error code for programmatic handling"
}
```

**Error Response (500 Internal Server Error)**:
```json
{
  "error": "string - Error message describing the server issue",
  "code": "string - Error code for programmatic handling"
}
```

## Error Codes

- `QUERY_TOO_LONG`: The query exceeds the maximum allowed length
- `INVALID_QUERY`: The query is malformed or empty
- `RAG_SERVICE_UNAVAILABLE`: The RAG backend is not responding
- `INTERNAL_ERROR`: An unexpected error occurred on the server

## Authentication

This API does not require authentication for basic query functionality.

## Rate Limiting

The API may implement rate limiting to prevent abuse. Clients should handle 429 responses gracefully.

## CORS Policy

The API should allow requests from the Docusaurus frontend origin to enable browser-based requests.