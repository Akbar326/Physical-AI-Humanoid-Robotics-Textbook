# Data Model: RAG Chatbot for Docusaurus

## Document Entity
**Description**: Represents a document chunk from the documentation site that has been processed and embedded for semantic search.

**Fields**:
- `id`: Unique identifier for the document chunk (UUID)
- `content`: The text content of the document chunk
- `source_url`: URL where the original content was found
- `title`: Title of the document page
- `embedding`: Vector representation of the content (array of floats)
- `metadata`: Additional metadata (author, date, etc.)

**Validation rules**:
- Content must not be empty
- Source URL must be a valid URL
- Embedding must be a valid vector of the expected dimension

## Query Entity
**Description**: Represents a user query to the RAG system.

**Fields**:
- `query_text`: The natural language query from the user
- `session_id`: Optional session identifier for conversation context
- `top_k`: Number of relevant documents to retrieve (default: 5)

**Validation rules**:
- Query text must not be empty
- Top_k must be between 1 and 20

## QueryResponse Entity
**Description**: Represents the response from the RAG system to a user query.

**Fields**:
- `answer`: The generated answer based on retrieved documents
- `sources`: List of source documents used to generate the answer
- `query_time`: Time taken to process the query
- `session_id`: Session identifier if applicable

**Validation rules**:
- Answer must not be empty
- Sources must be a valid list of document references

## VectorStore Entity
**Description**: Represents the vector store containing all embedded documentation content.

**Fields**:
- `documents`: Collection of Document entities
- `index`: FAISS index for similarity search
- `metadata`: Information about the vector store (creation date, source, etc.)

**State transitions**:
- Created during initial ingestion
- Updated when new content is added
- Replaced when content is regenerated