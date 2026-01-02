# Data Model: Website Deployment, Embeddings, and Vector Storage

## Entities

### BookContent
Represents the textual content extracted from book pages

**Fields**:
- `url` (string): The source URL of the content
- `title` (string): The title of the page
- `content` (string): The clean text content extracted from the page
- `created_at` (datetime): Timestamp when the content was extracted
- `updated_at` (datetime): Timestamp when the content was last updated

### TextChunk
Represents a chunk of text that will be embedded

**Fields**:
- `id` (string): Unique identifier for the chunk
- `content` (string): The text content of the chunk
- `source_url` (string): The original URL where this content came from
- `chunk_index` (integer): The position of this chunk in the original document
- `metadata` (dict): Additional metadata about the chunk

### EmbeddingVector
Represents the vector embedding of a text chunk

**Fields**:
- `chunk_id` (string): Reference to the original text chunk
- `vector` (list[float]): The embedding vector from Cohere
- `model_name` (string): The name of the model used for embedding
- `created_at` (datetime): Timestamp when the embedding was generated

### QdrantRecord
Represents a record stored in Qdrant vector database

**Fields**:
- `id` (string): Unique identifier in Qdrant
- `payload` (dict): Metadata associated with the vector (includes source_url, title, etc.)
- `vector` (list[float]): The embedding vector
- `collection_name` (string): The Qdrant collection name ("rag_embedding")

## Relationships

1. One `BookContent` can generate multiple `TextChunk` instances (when content is chunked)
2. One `TextChunk` maps to one `EmbeddingVector` (after embedding)
3. One `EmbeddingVector` becomes one `QdrantRecord` (when stored)

## Validation Rules

1. `BookContent.url` must be a valid URL format
2. `BookContent.content` must not be empty after extraction
3. `TextChunk.content` must be within Cohere's input token limits
4. `EmbeddingVector.vector` must match the expected dimensions for the model used
5. `QdrantRecord.collection_name` must be "rag_embedding" as specified