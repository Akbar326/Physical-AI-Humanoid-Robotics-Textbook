# Updated RAG Chatbot Implementation with OpenAI Agents SDK

## Overview
The RAG chatbot system has been updated to incorporate the OpenAI Agents SDK, providing enhanced reasoning capabilities on top of the existing RAG infrastructure.

## Key Changes

### 1. OpenAI Agents SDK Integration
- Replaced the OpenAI Assistants API with the new OpenAI Agents SDK
- Implemented function tools for documentation search
- Used the Runner.run() pattern for executing agent queries

### 2. Agent Architecture
- Created a function tool (`search_documentation_tool`) that the agent can use to search documentation
- Agent is configured with instructions to use the search tool when answering questions
- Maintains the same RAG service for backend operations

### 3. Updated agent.py
- Uses `from agents import Agent, Runner, function_tool`
- Implements a function tool that interfaces with the existing RAG service
- Agent automatically uses the search tool when needed to retrieve documentation
- Maintains backward compatibility with fallback to regular RAG

### 4. Dependencies
- Updated requirements.txt to use `agents>=0.1.0` instead of openai client library
- Maintains all other dependencies for the RAG system (faiss, sentence-transformers, etc.)

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   FastAPI        │───▶│  AgentRAGService│
│   (Docusaurus)  │    │   (main.py)      │    │                 │
└─────────────────┘    └──────────────────┘    │  ┌─────────────┐ │
                                              │  │  Agent      │ │───▶ OpenAI
                                               │  │  (GPT-4)    │ │
                                               │  └─────────────┘ │
                                               │         │         │
                                               │  ┌─────────────┐ │
                                               │  │  Tools      │ │
                                               │  │  (search_   │ │───▶ RAG Service
                                               │  │  documentation│ │
                                               │  │  _tool)     │ │
                                               │  └─────────────┘ │
                                               └──────────────────┘
                                                      │
                                               ┌─────────────────┐
                                               │   RAG Service   │
                                               │   (services/    │───▶ Vector Store
                                               │   rag.py)       │    (FAISS)
                                               └─────────────────┘
                                                      │
                                               ┌─────────────────┐
                                               │  Content        │
                                               │  Extraction     │───▶ Documentation
                                               │  & Chunking     │    (Sitemap)
                                               └─────────────────┘
```

## API Endpoints

### Traditional RAG Query
- **Endpoint**: `POST /query`
- **Function**: Direct RAG query without agent reasoning
- **Use Case**: Simple, fast queries where advanced reasoning isn't needed

### Agent-Enhanced Query
- **Endpoint**: `POST /agent-query`
- **Function**: Agent-based query with advanced reasoning capabilities
- **Use Case**: Complex queries requiring multi-step reasoning or synthesis of multiple sources

## Features

### 1. Function Tools
- `search_documentation_tool`: Allows the agent to search documentation when needed
- Tool returns structured results with title, URL, and content
- Content is truncated to prevent token overflow

### 2. Enhanced Reasoning
- Agent can perform multi-step reasoning using retrieved context
- Better handling of complex, multi-part questions
- Improved synthesis of information from multiple sources

### 3. Backward Compatibility
- Original RAG functionality preserved at `/query` endpoint
- Agent functionality added at `/agent-query` endpoint
- Fallback mechanism maintains system reliability

### 4. Error Handling
- Comprehensive error handling with fallback to regular RAG
- Detailed logging for debugging and monitoring
- Graceful degradation when agent service unavailable

## Implementation Details

### Agent Configuration
```python
self.agent = Agent(
    name="Documentation RAG Assistant",
    instructions="""
    You are a helpful documentation assistant. Use the search_documentation_tool to find relevant information
    from the documentation when answering questions. Always cite specific sections from the documentation
    in your responses. If the answer is not in the retrieved context, clearly state that the information
    is not available in the documentation.
    """,
    model="gpt-4-turbo",
    tools=[search_documentation_tool]
)
```

### Function Tool Implementation
```python
@function_tool
async def search_documentation_tool(query: str, top_k: int = 5) -> List[Dict[str, str]]:
    """
    Search the documentation for information related to the query.
    Returns a list of documents with title, URL, and content.
    """
    rag_result = await self.rag_service.query(query, top_k=top_k)
    return [
        {
            "title": source["title"],
            "url": source["url"],
            "content": source["content"][:500] + "..." if len(source["content"]) > 500 else source["content"]
        }
        for source in rag_result["sources"]
    ]
```

## Benefits

1. **Enhanced Reasoning**: Agents can perform complex reasoning using documentation context
2. **Tool Usage**: Automatic use of documentation search when needed
3. **Maintainability**: Clean separation between agent logic and RAG backend
4. **Scalability**: Can handle complex queries requiring multi-step processing
5. **Reliability**: Fallback to traditional RAG ensures system availability

## Usage

### For Complex Queries Requiring Reasoning
Use the `/agent-query` endpoint:
```bash
curl -X POST http://localhost:8000/agent-query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Compare the different approaches mentioned in the documentation and explain which is best for my use case?",
    "top_k": 5
  }'
```

### For Simple Direct Queries
Use the traditional `/query` endpoint:
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the basic setup process?",
    "top_k": 5
  }'
```

## Performance Considerations

- Agent queries may take longer due to multi-step processing
- Traditional RAG queries remain fast for simple questions
- Tool usage adds minimal overhead
- Vector store performance remains unchanged

## Deployment

The system maintains the same deployment requirements as before:
- Environment variables: OPENAI_API_KEY, SITEMAP_URL, PORT
- Compatible with Railway, Render, Fly.io
- Docker configuration unchanged
- Same ingestion process using `python -m scripts.ingest`