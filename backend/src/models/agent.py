"""
Agent-related models for the RAG Agent API
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from .search import RetrievedContext


class AgentContext(BaseModel):
    """
    Model for the context used by the RAG agent
    """
    query: str = Field(..., description="The original user query")
    retrieved_chunks: List[RetrievedContext] = Field(default=[], description="Context retrieved from vector store")
    formatted_prompt: Optional[str] = Field(default=None, description="The prompt formatted for the OpenAI agent")
    raw_response: Optional[str] = Field(default=None, description="Raw response from OpenAI agent")