# Data Model: RAG Chatbot Integration

## ChatMessage Entity

**Definition**: Represents a single message in the chat conversation

**Fields**:
- `id`: String (unique identifier for the message)
- `sender`: String ("user" | "assistant") - indicates who sent the message
- `content`: String - the actual message content
- `timestamp`: Date - when the message was created
- `sources`: Array<String> (optional) - source references for assistant responses

**Validation Rules**:
- `id` must be unique within the chat session
- `sender` must be either "user" or "assistant"
- `content` must not be empty
- `timestamp` must be a valid date

## ChatHistory Entity

**Definition**: Collection of ChatMessage entities representing the conversation

**Fields**:
- `sessionId`: String - unique identifier for the chat session
- `messages`: Array<ChatMessage> - ordered list of messages
- `createdAt`: Date - when the session was started
- `updatedAt`: Date - when the session was last updated

**Validation Rules**:
- `messages` must maintain chronological order
- `sessionId` should be generated uniquely per session

## QueryRequest Entity

**Definition**: Data structure for sending user queries to the RAG API

**Fields**:
- `query`: String - the user's question/query
- `sessionId`: String (optional) - session identifier for context
- `context`: Object (optional) - additional context for the query

**Validation Rules**:
- `query` must not be empty
- `query` length should be reasonable (e.g., < 1000 characters)

## QueryResponse Entity

**Definition**: Data structure for receiving responses from the RAG API

**Fields**:
- `response`: String - the AI-generated response
- `sources`: Array<Object> - references to source documents used
- `sessionId`: String (optional) - session identifier returned
- `timestamp`: Date - when the response was generated

**Validation Rules**:
- `response` must not be empty
- `sources` should contain relevant citation information

## API Configuration Entity

**Definition**: Configuration parameters for API integration

**Fields**:
- `baseUrl`: String - base URL for the RAG API
- `timeout`: Number - request timeout in milliseconds
- `headers`: Object - additional headers for API requests

**Validation Rules**:
- `baseUrl` must be a valid URL
- `timeout` must be a positive number