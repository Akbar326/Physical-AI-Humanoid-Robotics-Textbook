"""
OpenAI Agent implementation for the RAG chatbot system.
This agent enhances the RAG system by providing more sophisticated reasoning
capabilities on top of the retrieved documentation context.
"""
import asyncio
import os
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from agents import Agent, Runner, function_tool
from .models.query import QueryRequest, QueryResponse, SourceDocument
from .services.rag import RAGService
from .utils.logging import app_logger
from agents import OpenAIChatCompletionModel
from openai import AsyncOpenAI

ROUTER_API_KEY = "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"


Client = AsyncOpenAI(
    api_key=ROUTER_API_KEY,
    api_base="https://openrouter.ai/api/v1",
)

third_party_model = OpenAIChatCompletionModel(
    openai_client=Client,
    model="mistralai/devstral-2512:free",
)


@function_tool
async def search_documentation(query: str, top_k: int = 5) -> List[Dict[str, str]]:
    """
    Search the documentation for information related to the query.
    This function is available as a tool for the agent to use.
    """
    # We'll need to make this work differently - let's create a separate service
    # that can be used both directly and as a function tool
    pass


class AgentRAGService:
    """
    Enhanced RAG service that uses OpenAI Agents SDK for more sophisticated reasoning
    on top of the retrieved documentation context.
    """

    def __init__(self):
        self.rag_service = RAGService()
        # Create a function tool for the agent to use for searching documentation
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
                    "content": source["content"][:500] + "..." if len(source["content"]) > 500 else source["content"]  # Truncate long content
                }
                for source in rag_result["sources"]
            ]

        # Initialize the agent with instructions and tools
        self.agent = Agent(
            name="Documentation RAG Assistant",
            instructions="""
            You are a helpful documentation assistant. Use the search_documentation_tool to find relevant information
            from the documentation when answering questions. Always cite specific sections from the documentation
            in your responses. If the answer is not in the retrieved context, clearly state that the information
            is not available in the documentation.
            """,
            model=third_party_model,
            tools=[search_documentation_tool]
        )

    async def query_with_agent(self, query_request: QueryRequest) -> QueryResponse:
        """
        Process a query using the OpenAI Agent enhanced RAG approach.
        The agent will use the search_documentation_tool to find relevant information.
        """
        try:
            # Run the agent with the user query - the agent will automatically use the search tool as needed
            result = await Runner.run(self.agent, query_request.query)

            # Extract the agent's response
            agent_response = result.final_output

            # Since the agent uses tools, we need to extract the sources from the run steps
            # For now, we'll run a separate search to get the sources for the response
            rag_result = await self.rag_service.query(query_request.query, top_k=query_request.top_k)

            # Format response with sources from RAG
            sources = [
                SourceDocument(
                    title=source["title"],
                    url=source["url"],
                    content=source["content"]
                )
                for source in rag_result["sources"]
            ]

            return QueryResponse(
                answer=agent_response,
                sources=sources,
                query_time=0.0,  # Placeholder - would need to track properly
                session_id=query_request.session_id
            )

        except Exception as e:
            app_logger.error(f"Error in agent query: {str(e)}")
            # Fallback to regular RAG on error
            return await self._fallback_to_regular_rag(query_request)


    async def _fallback_to_regular_rag(self, query_request: QueryRequest, start_time: Optional[float] = None) -> QueryResponse:
        """
        Fallback to regular RAG service if agent is not available.
        """
        import time

        if start_time is None:
            start_time = time.time()

        rag_result = await self.rag_service.query(query_request.query, top_k=query_request.top_k)
        query_time = time.time() - start_time

        sources = [
            SourceDocument(
                title=source["title"],
                url=source["url"],
                content=source["content"]
            )
            for source in rag_result["sources"]
        ]

        return QueryResponse(
            answer=rag_result["answer"],
            sources=sources,
            query_time=query_time,
            session_id=query_request.session_id
        )

    async def load_vector_store(self):
        """
        Load the vector store through the underlying RAG service.
        """
        await self.rag_service.load_vector_store()

    async def ingest_sitemap(self, sitemap_url: str, force_rebuild: bool = False):
        """
        Ingest sitemap through the underlying RAG service.
        """
        await self.rag_service.ingest_sitemap(sitemap_url, force_rebuild)


# Example usage function
async def example_usage():
    """
    Example of how to use the AgentRAGService.
    """
    agent_service = AgentRAGService()

    # Load the vector store
    await agent_service.load_vector_store()

    # Create a query request
    query_request = QueryRequest(
        query="What are the key features of this documentation system?",
        top_k=3
    )

    # Process with agent-enhanced RAG
    response = await agent_service.query_with_agent(query_request)

    print("Agent Response:", response.answer)
    print("Sources:", [source.title for source in response.sources])


if __name__ == "__main__":
    # Run example if executed directly
    asyncio.run(example_usage())