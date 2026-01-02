"""
Search-related models for the RAG Agent API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Citation(BaseModel):
    """
    Model for citations in the RAG agent response
    """
    url: str = Field(..., description="URL of the source document")
    title: str = Field(..., description="Title of the source document")
    score: float = Field(..., description="Relevance score from vector search")


class RetrievedContext(BaseModel):
    """
    Model for retrieved context chunks
    """
    content: str = Field(..., description="The retrieved text content")
    url: str = Field(..., description="URL of the source")
    title: str = Field(..., description="Title of the source document")
    score: float = Field(..., description="Relevance score from vector search")


class SearchQuery(BaseModel):
    """
    Model for internal search queries
    """
    text: str = Field(..., description="The search query text")
    top_k: int = Field(5, description="Number of results to retrieve", ge=1, le=20)
    filters: Optional[Dict[str, Any]] = Field(default={}, description="Optional filters for search")