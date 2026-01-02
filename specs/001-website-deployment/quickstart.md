# Quickstart Guide: RAG Pipeline Backend

## Prerequisites

- Python 3.11+
- UV package manager
- Cohere API key
- Qdrant Cloud credentials

## Setup

1. **Create the backend directory:**
   ```bash
   mkdir backend
   cd backend
   ```

2. **Create requirements.txt:**
   ```txt
   cohere==5.5.3
   qdrant-client==1.9.0
   beautifulsoup4==4.12.2
   requests==2.31.0
   python-dotenv==1.0.0
   ```

3. **Install dependencies using UV:**
   ```bash
   uv pip install -r requirements.txt
   # Or if using a virtual environment:
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

4. **Create .env file with your credentials:**
   ```env
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   QDRANT_HOST=your_qdrant_cluster_url
   ```

5. **Create the main.py file with the implementation**

## Environment Configuration

Create a `config/settings.py` file to manage your configuration:

```python
import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")
BOOK_SITE_URL = "https://physical-ai-humanoid-robotics-textb-topaz-theta.vercel.app/"
```

## Running the Ingestion Pipeline

1. **Execute the main ingestion function:**
   ```bash
   python main.py
   ```

2. **The ingest_book function will:**
   - Get all URLs from the deployed Docusaurus site
   - Extract clean text from each URL
   - Chunk the text appropriately
   - Generate embeddings using Cohere
   - Create the "rag_embedding" collection in Qdrant
   - Save all chunks with embeddings to Qdrant

## Validation

After running the ingestion, you can validate the process by:

1. Checking that the "rag_embedding" collection exists in Qdrant
2. Verifying that records have been stored with proper metadata
3. Running a basic similarity search to ensure the embeddings work correctly