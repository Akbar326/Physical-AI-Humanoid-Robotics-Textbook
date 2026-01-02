# Data Models: Frontend-Backend Integration

## Request Models

### QueryRequest
- **query**: string (required) - The natural language query from the user
- **selectedText**: string (optional) - Text selected by the user for context-aware queries
- **includeCitations**: boolean (optional, default: true) - Whether to include source citations in response
- **maxResults**: integer (optional, default: 5) - Maximum number of context results to retrieve
- **temperature**: float (optional, default: 0.3) - Controls response creativity

### APIRequest
- **url**: string - The backend API endpoint URL
- **method**: string - HTTP method (GET, POST, PUT, DELETE)
- **headers**: object - HTTP headers for the request
- **body**: object - Request body for POST/PUT requests
- **timeout**: integer (optional, default: 30000) - Request timeout in milliseconds

## Response Models

### QueryResponse
- **query**: string - Echo of the original query
- **answer**: string - The agent's response grounded in retrieved context
- **citations**: array of Citation objects - Sources used in the response
- **retrievedContexts**: array of RetrievedContext objects - Full context snippets retrieved
- **executionTime**: float - Time taken to process the request in seconds
- **success**: boolean - Whether the request was processed successfully
- **error**: object (optional) - Error details if the request failed

### Citation
- **url**: string - URL of the source document
- **title**: string - Title of the source document
- **score**: float - Relevance score from vector search

### RetrievedContext
- **content**: string - The retrieved text content
- **url**: string - URL of the source
- **title**: string - Title of the source document
- **score**: float - Relevance score from vector search

## Frontend State Models

### QueryState
- **query**: string - Current query text in the input field
- **selectedText**: string - Currently selected text from the book content
- **isLoading**: boolean - Whether an API request is in progress
- **response**: QueryResponse (optional) - The response from the last query
- **error**: string (optional) - Error message if the last query failed
- **history**: array of QueryHistoryItem objects - History of previous queries

### QueryHistoryItem
- **id**: string - Unique identifier for the history item
- **query**: string - The original query text
- **timestamp**: string - ISO date string of when the query was made
- **response**: QueryResponse - The response from the query

## UI Component Props

### RagQueryFormProps
- **onSubmit**: function (required) - Callback function when query is submitted
- **onTextSelection**: function (required) - Callback function when text is selected
- **defaultValue**: string (optional) - Default query text
- **placeholder**: string (optional, default: "Ask a question about this book...") - Input field placeholder
- **disabled**: boolean (optional, default: false) - Whether the form is disabled

### RagQueryResultProps
- **response**: QueryResponse (optional) - The response to display
- **isLoading**: boolean (optional, default: false) - Whether to show loading state
- **error**: string (optional) - Error message to display
- **onRetry**: function (optional) - Callback function to retry the query

### RagQueryContextProps
- **onTextSelect**: function (required) - Callback function when text is selected
- **children**: ReactNode - Child components to wrap with text selection functionality

## Validation Rules

### QueryRequest Validation
- query must be between 1 and 1000 characters
- maxResults must be between 1 and 20
- temperature must be between 0.0 and 1.0
- query must not contain potentially harmful content (XSS prevention)

### Response Validation
- answer must be grounded in the retrieved context
- citations must correspond to actual retrieved documents
- response time should be under 5 seconds for 95% of requests

## State Transitions

### Query Processing Flow
1. **Idle**: Initial state with empty query field
2. **Input**: User is typing a query or has selected text
3. **Submitting**: Query is being sent to the backend API
4. **Loading**: Waiting for response from the backend
5. **Success**: Response received and displayed
6. **Error**: Error occurred, error message displayed
7. **History**: Previous query available for reference