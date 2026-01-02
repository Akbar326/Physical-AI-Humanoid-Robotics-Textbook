# Quickstart Guide: RAG Agent and API Service

## Prerequisites

- Python 3.11+
- pip package manager
- Access to OpenAI API key
- Access to Qdrant vector database (existing setup)
- Existing book content already ingested into Qdrant

## Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-humanoid-robotics
   ```

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn openai python-dotenv
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the backend directory with:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   COHERE_API_KEY=your_cohere_api_key_here  # From existing setup
   QDRANT_API_KEY=your_qdrant_api_key_here  # From existing setup
   QDRANT_HOST=your_qdrant_host_here        # From existing setup
   COLLECTION_NAME=rag_embedding            # From existing setup
   ```

## Running the Service

1. **Start the API server**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Verify the service is running**
   Open your browser to `http://localhost:8000/docs` to access the Swagger UI documentation.

## API Usage

### Query the RAG Agent

**Endpoint**: `POST /api/v1/query`

**Request Body**:
```json
{
  "query": "What are the key concepts in AI robotics?",
  "max_results": 5,
  "include_citations": true,
  "temperature": 0.3
}
```

**Example cURL command**:
```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key concepts in AI robotics?",
    "max_results": 5,
    "include_citations": true,
    "temperature": 0.3
  }'
```

**Expected Response**:
```json
{
  "query": "What are the key concepts in AI robotics?",
  "answer": "AI robotics combines artificial intelligence with robotics to create autonomous systems...",
  "citations": [
    {
      "url": "https://example-book.com/ai-robotics/concepts",
      "title": "AI Robotics Concepts",
      "score": 0.85
    }
  ],
  "retrieved_contexts": [
    {
      "content": "AI robotics is an interdisciplinary field that combines...",
      "url": "https://example-book.com/ai-robotics/concepts",
      "title": "AI Robotics Concepts",
      "score": 0.85
    }
  ],
  "execution_time": 2.34,
  "success": true
}
```

## Testing the Service

1. **Run unit tests**
   ```bash
   pytest tests/unit/
   ```

2. **Run integration tests**
   ```bash
   pytest tests/integration/
   ```

3. **Test with sample queries**
   ```bash
   python -c "
   import requests
   response = requests.post('http://localhost:8000/api/v1/query', json={
       'query': 'What is physical AI?',
       'max_results': 3
   })
   print(response.json())
   "
   ```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for agent functionality
- `QDRANT_HOST`: URL of your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant access
- `COLLECTION_NAME`: Name of the Qdrant collection (default: rag_embedding)
- `API_HOST`: Host for the API server (default: 0.0.0.0)
- `API_PORT`: Port for the API server (default: 8000)
- `MAX_CONCURRENT_REQUESTS`: Maximum concurrent requests (default: 100)

### Default Settings

- Response timeout: 30 seconds
- Maximum query length: 1000 characters
- Default max_results: 5
- Default temperature: 0.3
- Default include_citations: true

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your OpenAI API key is valid and has sufficient quota
   - Check that the environment variable is set correctly

2. **Qdrant Connection Issues**
   - Verify that your Qdrant instance is running and accessible
   - Check that the host and API key are configured correctly
   - Ensure the collection exists and has ingested content

3. **Slow Responses**
   - Check that book content has been properly ingested into Qdrant
   - Verify that your OpenAI API key has sufficient rate limits
   - Monitor system resources during high load

### Health Check

Check the health of your service:
```bash
curl http://localhost:8000/health
```

Expected response: `{"status": "healthy", "timestamp": "2025-12-23T10:00:00Z"}`