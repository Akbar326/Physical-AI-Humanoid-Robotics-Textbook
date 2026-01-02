# Quickstart: RAG Chatbot for Docusaurus

## Prerequisites
- Python 3.11+
- Access to OpenAI API key
- Sitemap URL for your documentation

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

3. **Create virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your values:
   # OPENAI_API_KEY=your_openai_api_key
   # SITEMAP_URL=https://your-docs-site.com/sitemap.xml
   # PORT=8000
   ```

5. **Generate embeddings from your sitemap**
   ```bash
   python -m scripts.ingest
   # This will fetch content from your sitemap and create vector embeddings
   ```

6. **Start the server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

## API Usage

### Query the RAG system
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does this documentation cover?",
    "top_k": 5
  }'
```

### Check health
```bash
curl http://localhost:8000/health
```

## Frontend Integration

To integrate with your Docusaurus site:

1. Add the chatbot component to your site
2. Configure the backend API URL in the frontend
3. The component will make requests to your deployed backend

## Deployment

### To Railway
1. Create a new app on Railway
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables: OPENAI_API_KEY, SITEMAP_URL

### To Render
1. Create a new web service on Render
2. Set the runtime to Python
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables: OPENAI_API_KEY, SITEMAP_URL