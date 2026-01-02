# Data Models: RAG Agent and API Service

## Request Models

### QueryRequest
- **query**: string (required) - The natural language query from the user
- **max_results**: integer (optional, default: 5) - Maximum number of context results to retrieve
- **include_citations**: boolean (optional, default: true) - Whether to include source citations in response
- **temperature**: float (optional, default: 0.3) - Controls response creativity

### QueryResponse
- **query**: string - Echo of the original query
- **answer**: string - The agent's response grounded in retrieved context
- **citations**: array of Citation objects - Sources used in the response
- **retrieved_contexts**: array of RetrievedContext objects - Full context snippets retrieved
- **execution_time**: float - Time taken to process the request in seconds
- **success**: boolean - Whether the request was processed successfully

## Response Models

### Citation
- **url**: string - URL of the source document
- **title**: string - Title of the source document
- **score**: float - Relevance score from vector search

### RetrievedContext
- **content**: string - The retrieved text content
- **url**: string - URL of the source
- **title**: string - Title of the source document
- **score**: float - Relevance score from vector search

## Internal Models

### AgentContext
- **query**: string - The original user query
- **retrieved_chunks**: array of Qdrant search results - Context retrieved from vector store
- **formatted_prompt**: string - The prompt formatted for the OpenAI agent
- **raw_response**: string - Raw response from OpenAI agent

### SearchQuery
- **text**: string - The search query text
- **top_k**: integer - Number of results to retrieve
- **filters**: dict - Optional filters for search

## Validation Rules

### QueryRequest Validation
- query must be between 1 and 1000 characters
- max_results must be between 1 and 20
- temperature must be between 0.0 and 1.0
- query must not contain SQL injection patterns or other malicious content

### Response Validation
- answer must be grounded in the retrieved context
- citations must correspond to actual retrieved documents
- response time should be under 5 seconds for 95% of requests

## State Transitions

### Query Processing Flow
1. **Received**: QueryRequest validated and accepted
2. **Retrieving**: Context retrieved from Qdrant based on the query
3. **Processing**: OpenAI agent processes query with retrieved context
4. **Formatting**: Response formatted with citations and metadata
5. **Completed**: QueryResponse returned to the user

## Entity Relationships

- QueryRequest → AgentContext (1:1) - Each request creates one agent context
- AgentContext → RetrievedContext (1:many) - Agent context contains multiple retrieved contexts
- RetrievedContext → Citation (1:1) - Each retrieved context has one citation
- QueryResponse → Citation (1:many) - Response can contain multiple citations