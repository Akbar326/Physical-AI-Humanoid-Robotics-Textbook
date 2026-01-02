# RAG Chatbot Backend

This is the backend server for the RAG (Retrieval Augmented Generation) chatbot that integrates with Docusaurus documentation sites.

## Features

- Sitemap-based documentation ingestion
- Vector storage using FAISS
- OpenAI-powered query processing
- FastAPI-based REST API
- Lightweight design for deployment on Railway/Render/Fly.io

## Prerequisites

- Python 3.11+
- OpenAI API key

## Setup

1. Clone the repository
2. Navigate to the backend directory: `cd backend`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Create a `.env` file with your configuration:

```bash
OPENAI_API_KEY=your_openai_api_key_here
SITEMAP_URL=https://your-docs-site.com/sitemap.xml
PORT=8000
```

## Usage

### Pre-generating Embeddings

Before starting the server, you should pre-generate embeddings from your documentation:

```bash
python -m scripts.ingest
```

This will fetch content from your sitemap URL, generate embeddings, and save them to the vector store.

### Starting the Server

```bash
python run_server.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /query` - Submit a query to the traditional RAG system
- `POST /agent-query` - Submit a query to the Agent-enhanced RAG system for more sophisticated reasoning
- `POST /ingest` - Trigger the ingestion process

### Query Endpoint

```json
{
  "query": "Your question about the documentation",
  "session_id": "optional-session-id",
  "top_k": 5
}
```

### Ingest Endpoint

```json
{
  "sitemap_url": "https://your-site.com/sitemap.xml",
  "force_rebuild": false
}
```

## Deployment

### Railway

1. Create a new app on Railway
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables: OPENAI_API_KEY, SITEMAP_URL

### Render

1. Create a new web service on Render
2. Set the runtime to Python
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables: OPENAI_API_KEY, SITEMAP_URL

## Architecture

- `main.py` - FastAPI application entry point
- `models/` - Pydantic models for requests and responses
- `services/` - Business logic (RAG processing)
- `storage/` - Vector store operations
- `utils/` - Utility functions (sitemap parsing, content extraction)
- `scripts/` - CLI scripts (ingestion)

## Configuration

The application uses environment variables for configuration:

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `SITEMAP_URL` - URL to your documentation sitemap.xml (required)
- `PORT` - Port to run the server on (default: 8000)