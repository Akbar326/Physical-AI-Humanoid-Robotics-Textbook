# Research: RAG Chatbot for Docusaurus

## Decision: Python-based RAG Architecture
**Rationale**: Python is ideal for RAG applications due to the rich ecosystem of libraries for NLP, embeddings, and vector databases. FastAPI provides an efficient async framework for handling concurrent requests, while libraries like sentence-transformers and FAISS provide robust embedding and similarity search capabilities.

**Alternatives considered**:
- Node.js with TypeScript - Less mature ecosystem for NLP tasks
- Go - Less suitable for ML/AI tasks
- Rust - More complex for this use case

## Decision: Vector Database Selection (FAISS vs Pinecone vs others)
**Rationale**: FAISS (Facebook AI Similarity Search) is chosen for local deployment because it's lightweight, efficient, and doesn't require external service dependencies. This addresses the requirement for lightweight deployment on Railway/Render. Pre-generating embeddings means we only need to load the vector store at runtime.

**Alternatives considered**:
- Pinecone - Cloud-based, requires subscription and external dependencies
- Weaviate - More complex setup, potential memory overhead
- ChromaDB - Simpler but potentially less performant for production use

## Decision: Embedding Model Selection
**Rationale**: Using OpenAI embeddings API for consistency and quality, but with pre-generation to minimize runtime costs and latency. Alternatively, open-source models like sentence-transformers/all-MiniLM-L6-v2 can be used for completely self-hosted solution.

**Alternatives considered**:
- OpenAI embeddings API - Higher cost but high quality
- Sentence-transformers local models - Free but requires more memory at generation time
- Hugging Face models - Various options with different trade-offs

## Decision: Sitemap Ingestion Strategy
**Rationale**: The system will parse the sitemap.xml to extract URLs, then fetch and parse HTML content from each URL to extract text content for embedding. This approach ensures all documentation pages are indexed.

**Alternatives considered**:
- Direct file parsing - Requires access to source files
- API-based content extraction - Requires documentation platform to provide API
- Manual content upload - Not scalable

## Decision: Frontend Integration Approach
**Rationale**: The chatbot interface will be implemented as a floating widget or sidebar component that can be easily integrated into Docusaurus sites using React components. The frontend will communicate with the backend via REST API calls.

**Alternatives considered**:
- Iframe embedding - More isolated but less integrated
- Server-side includes - More complex deployment
- Native Docusaurus plugin - More complex development but more integrated

## Decision: Deployment Configuration
**Rationale**: Using environment variables for configuration (OPENAI_API_KEY, SITEMAP_URL, etc.) with a $PORT variable for deployment compatibility. The uvicorn command will be configured to use 0.0.0.0:host and $PORT as required.

**Alternatives considered**:
- Hardcoded configuration - Less flexible
- Configuration files - More complex for deployment platforms
- Database configuration - Overkill for this use case