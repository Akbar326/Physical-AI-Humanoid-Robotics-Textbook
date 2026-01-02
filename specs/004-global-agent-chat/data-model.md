# Data Model: Global Agent-Only Chat

## Entities

### ChatMessage
- **id**: string (unique identifier for the message)
- **sender**: string (either "user" or "agent")
- **content**: string (the text content of the message)
- **timestamp**: Date (when the message was sent/received)
- **status**: string (optional - "sending", "sent", "error")

### ChatState
- **isOpen**: boolean (whether the chat UI is expanded or collapsed)
- **messages**: array of ChatMessage (conversation history)
- **isLoading**: boolean (whether an agent response is being fetched)
- **error**: string or null (any error message from the agent service)

### AgentQueryRequest
- **query**: string (the user's question/query)
- **session_id**: string or null (optional session identifier)

### AgentQueryResponse
- **answer**: string (the agent's response)
- **sources**: array of objects (relevant sources cited in the response)
- **query_time**: number (time taken for the query in seconds)
- **session_id**: string or null (session identifier)

## Relationships

- ChatState contains multiple ChatMessage entities
- ChatMessage is associated with a single ChatState
- AgentQueryRequest and AgentQueryResponse are used for API communication

## Validation Rules

- ChatMessage content must not be empty
- ChatMessage sender must be either "user" or "agent"
- AgentQueryRequest query must not be empty
- ChatState messages array must have a reasonable size limit (e.g., 100 messages)

## State Transitions

- ChatState.isOpen: false ↔ true (toggle via user interaction)
- ChatMessage.status: null → "sending" → "sent" (message transmission flow)
- ChatState.isLoading: false → true → false (during agent request/response cycle)
- ChatState.error: null ↔ string (when errors occur and are cleared)