# RAG Agent API

The RAG (Retrieval-Augmented Generation) Agent API provides a REST interface for querying book content through an AI agent that retrieves relevant information from a vector database and generates responses grounded in the retrieved context.

## Setup

### Prerequisites

- Python 3.11+
- pip package manager
- Access to OpenAI API key
- Access to Qdrant vector database
- Existing book content already ingested into Qdrant

### Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the backend directory with:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_HOST=your_qdrant_host_here
   COLLECTION_NAME=rag_embedding
   ```

## Running the Service

Start the API server:
```bash
cd backend
python run_server.py
```

Or directly with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## API Usage

### Query Endpoint

**POST** `/api/v1/query`

Submit a natural language query to the RAG agent, which will retrieve relevant book content and generate a response grounded in that context.

#### Request Body

```json
{
  "query": "What are the key concepts in AI robotics?",
  "max_results": 5,
  "include_citations": true,
  "temperature": 0.3
}
```

**Fields**:
- `query`: (string, required) The natural language query from the user (1-1000 characters)
- `max_results`: (integer, optional) Maximum number of context results to retrieve (1-20, default: 5)
- `include_citations`: (boolean, optional) Whether to include source citations in response (default: true)
- `temperature`: (number, optional) Controls response creativity (0.0-1.0, default: 0.3)

#### Example Request

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

#### Response

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

### Health Check Endpoint

**GET** `/api/v1/health`

Check the health status of the API service.

#### Response

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

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for agent functionality
- `QDRANT_HOST`: URL of your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant access
- `COLLECTION_NAME`: Name of the Qdrant collection (default: rag_embedding)
- `API_HOST`: Host for the API server (default: 0.0.0.0)
- `API_PORT`: Port for the API server (default: 8000)
- `MAX_CONCURRENT_REQUESTS`: Maximum concurrent requests (default: 100)

## Testing

Run the comprehensive test suite:
```bash
python test_comprehensive.py
```

Run specific tests:
```bash
python test_queries.py
```

## Error Handling

The API handles various error conditions:

- **400 Bad Request**: Invalid request parameters
- **422 Unprocessable Entity**: Validation errors
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Processing errors
- **503 Service Unavailable**: Downstream service unavailable

Rate limiting is enforced at 100 requests per minute per IP address. Exceeded requests will receive a 429 status code with rate limit headers.

## Architecture

The RAG Agent API consists of:

1. **Query Processing Pipeline**:
   - Query validation and sanitization
   - Query type detection (factual, analytical, comparative)
   - Context retrieval from Qdrant vector store
   - Response generation using OpenAI agent
   - Response formatting with citations

2. **Services**:
   - Qdrant search service for context retrieval
   - OpenAI agent service for response generation
   - Query analysis service for query type detection
   - Response validation service for quality assurance

3. **Utilities**:
   - Performance monitoring
   - Rate limiting
   - Circuit breaking for downstream services
   - Comprehensive error handling