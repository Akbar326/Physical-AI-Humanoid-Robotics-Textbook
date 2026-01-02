# Validation API Documentation

## Overview

The Validation API provides endpoints for testing and validating the retrieval pipeline functionality of the RAG (Retrieval-Augmented Generation) system. It allows developers to run semantic similarity searches, validate metadata accuracy, test edge cases, and ensure pipeline reliability.

## Base URL

```
http://localhost:8000/api/validation
```

## Authentication

No authentication required for validation endpoints.

## Endpoints

### 1. Validate Metadata

Validates metadata for search results.

#### `POST /validate`

Validates metadata for a list of search results.

**Request Body:**
```json
{
  "search_results": [
    {
      "chunk_id": "string",
      "content": "string",
      "source_url": "string"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "validation_results": [
    {
      "completeness_validation": {
        "success": true,
        "message": "string",
        "details": {}
      },
      "accuracy_validation": {
        "success": true,
        "message": "string",
        "details": {}
      },
      "metadata": {
        "chunk_id": "string",
        "content": "string",
        "url": "string"
      },
      "overall_valid": true
    }
  ],
  "summary": {
    "total_results": 0,
    "valid_results": 0,
    "invalid_results": 0,
    "metadata_accuracy": 0.0
  }
}
```

### 2. Validate Search Results with Metadata

Performs a search and validates metadata in one call.

#### `POST /validate-search-results`

Performs a search and validates metadata for the results.

**Request Body:**
```json
{
  "query_text": "string",
  "top_k": 5
}
```

**Response:**
```json
{
  "success": true,
  "search_results": {
    "results": [
      {
        "chunk_id": "string",
        "content": "string",
        "source_url": "string",
        "relevance_score": 0.0,
        "position": 0,
        "metadata": {}
      }
    ],
    "metadata_accuracy": 0.0,
    "metadata_validation_summary": {},
    "detailed_metadata_validation": [],
    "query": "string",
    "top_k": 0
  }
}
```

### 3. Validate Single Metadata Entry

Validates a single metadata entry.

#### `POST /validate-single-metadata`

Validates a single metadata entry.

**Request Body:**
```json
{
  "chunk_id": "string",
  "content": "string",
  "source_url": "string"
}
```

**Response:**
```json
{
  "success": true,
  "validation_result": {
    "completeness_validation": {},
    "accuracy_validation": {},
    "metadata": {},
    "overall_valid": true
  }
}
```

### 4. Extract Metadata

Extracts metadata from content.

#### `POST /extract-metadata`

Extracts metadata from provided content.

**Request Body:**
```json
{
  "content": "string",
  "source_url": "string"
}
```

**Response:**
```json
{
  "success": true,
  "extracted_metadata": {
    "content_length": 0,
    "word_count": 0,
    "character_count": 0,
    "contains_urls": ["string"],
    "contains_emails": ["string"],
    "first_paragraph": "string",
    "last_paragraph": "string",
    "source_url": "string"
  }
}
```

### 5. Validate Metadata Consistency

Validates consistency across multiple metadata entries.

#### `POST /validate-consistency`

Validates consistency across multiple metadata entries.

**Request Body:**
```json
{
  "metadata_list": [
    {
      "field1": "value1",
      "field2": "value2"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "consistency_result": {
    "consistent": true,
    "message": "string",
    "details": {}
  }
}
```

## Configuration

The validation service can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `VALIDATION_ENABLED` | Enable validation endpoints | `True` |
| `VALIDATION_TIMEOUT` | Timeout for validation operations (seconds) | `30.0` |
| `MAX_VALIDATION_RETRIES` | Maximum number of retries for validation | `3` |
| `METADATA_VALIDATION_ENABLED` | Enable metadata validation | `True` |
| `MIN_RELEVANCE_SCORE` | Minimum acceptable relevance score | `0.5` |
| `MAX_SEARCH_RESULTS` | Maximum number of search results to validate | `10` |
| `SEARCH_TIMEOUT` | Timeout for search operations (seconds) | `15.0` |
| `RESPONSE_TIME_THRESHOLD` | Maximum acceptable response time (seconds) | `5.0` |
| `SUCCESS_RATE_THRESHOLD` | Minimum acceptable success rate | `0.9` |

## Error Handling

The API follows standard HTTP error codes:

- `200`: Success
- `400`: Bad request (malformed input)
- `500`: Internal server error

## Performance Considerations

- Validation operations may take longer than regular search operations
- Use batch validation endpoints for multiple items to improve efficiency
- Monitor response times to ensure acceptable performance

## Examples

### Validate Search Results

```bash
curl -X POST http://localhost:8000/api/validation/validate-search-results \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "AI robotics fundamentals",
    "top_k": 5
  }'
```

### Validate Metadata

```bash
curl -X POST http://localhost:8000/api/validation/validate \
  -H "Content-Type: application/json" \
  -d '{
    "search_results": [
      {
        "chunk_id": "chunk_1",
        "content": "Sample content for validation",
        "source_url": "https://example.com"
      }
    ]
  }'
```

## Testing

The validation API includes comprehensive testing capabilities:

- Basic semantic search validation
- Metadata retrieval validation
- Retrieval pipeline reliability testing
- Edge case handling validation
- Performance benchmarking

## Troubleshooting

### Common Issues

1. **Timeout Errors**: Increase the `VALIDATION_TIMEOUT` environment variable
2. **Validation Failures**: Check that required metadata fields are present
3. **Performance Issues**: Review batch size and concurrency settings

### Debugging

Enable detailed logging by setting `LOG_LEVEL` to `DEBUG` to get more information about validation processes.