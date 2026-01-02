# Research Summary: Website Deployment, Embeddings, and Vector Storage

## Overview
This research document captures the technical decisions and findings for implementing the RAG pipeline for book content, including crawling the Docusaurus website, extracting content, generating embeddings with Cohere, and storing in Qdrant.

## Technology Decisions

### 1. Python as Implementation Language
**Decision**: Use Python 3.11+ with UV package manager
**Rationale**: Python is the standard for AI/ML applications and has excellent libraries for web scraping, embeddings, and vector databases
**Alternatives considered**:
- JavaScript/Node.js - Less suitable for ML tasks
- Go - Good performance but fewer ML libraries
- Rust - Great performance but steeper learning curve for this use case

### 2. Cohere for Embeddings
**Decision**: Use Cohere's embedding models
**Rationale**: Cohere provides high-quality embeddings optimized for search and retrieval tasks, with good documentation and Python SDK
**Alternatives considered**:
- OpenAI embeddings - More expensive, slightly different quality characteristics
- Hugging Face models - Self-hosted option but requires more infrastructure
- Sentence Transformers - Open source but requires model management

### 3. Qdrant for Vector Storage
**Decision**: Use Qdrant vector database
**Rationale**: Qdrant offers cloud hosting, good performance, Python SDK, and is designed for semantic search applications
**Alternatives considered**:
- Pinecone - Commercial alternative but more expensive
- Weaviate - Open source alternative with similar features
- ChromaDB - Simpler but less scalable for production use

### 4. BeautifulSoup for HTML Parsing
**Decision**: Use BeautifulSoup4 for extracting clean text content
**Rationale**: BeautifulSoup is the standard Python library for parsing HTML and extracting content, with good handling of malformed HTML
**Alternatives considered**:
- Scrapy - More complex but overkill for this simple scraping task
- Selenium - More heavy-handed, requires browser automation
- Regular expressions - Less reliable for HTML parsing

## Architecture Decisions

### 1. Single File Implementation
**Decision**: Implement all functionality in a single main.py file as specified
**Rationale**: For this specific ingestion pipeline, a single file keeps the implementation simple and focused
**Alternatives considered**:
- Modular approach with separate files - More complex but better for larger applications
- Package structure - Overkill for this simple ingestion task

### 2. Function Design
**Decision**: Implement the specific functions as requested:
- get_all_urls: Crawl the deployed Docusaurus site to get all page URLs
- extract_text_from_url: Extract clean text from each URL
- chunk_text: Split large texts into smaller chunks for embedding
- embed: Generate embeddings using Cohere
- create_collection: Create a Qdrant collection named "rag_embedding"
- save_chunk_to_qdrant: Store embeddings in Qdrant with metadata
- ingest_book: Main function that orchestrates the entire process

## Deployment URL Analysis
**Target**: https://physical-ai-humanoid-robotics-textb-topaz-theta.vercel.app/
**Approach**: The implementation will crawl this site to extract all available book content pages

## Environment Configuration
**Decision**: Use environment variables for Cohere and Qdrant credentials
**Rationale**: Keeps sensitive information secure and allows for different configurations per environment
**Implementation**: Store in .env file (gitignored) and load via configuration management

## Text Chunking Strategy
**Decision**: Implement text chunking to handle large documents
**Rationale**: Most embedding models have token limits, so large documents need to be split into smaller chunks
**Approach**: Use semantic chunking to keep related content together while respecting model limits

## Error Handling Strategy
**Decision**: Implement comprehensive error handling for network requests, API calls, and storage operations
**Rationale**: Web scraping and API calls are inherently unreliable, requiring robust error handling and retry logic