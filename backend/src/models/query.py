"""
Query request and response models for the RAG Agent API
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from .search import Citation, RetrievedContext


class QueryRequest(BaseModel):
    """
    Request model for querying the RAG agent
    """
    query: str = Field(
        ...,
        description="The natural language query from the user",
        min_length=1,
        max_length=1000
    )
    max_results: Optional[int] = Field(
        5,
        description="Maximum number of context results to retrieve",
        ge=1,
        le=20
    )
    include_citations: Optional[bool] = Field(
        True,
        description="Whether to include source citations in response"
    )
    temperature: Optional[float] = Field(
        0.3,
        description="Controls response creativity",
        ge=0.0,
        le=1.0
    )


class QueryResponse(BaseModel):
    """
    Response model for the RAG agent query
    """
    query: str = Field(..., description="Echo of the original query")
    answer: str = Field(..., description="The agent's response grounded in retrieved context")
    citations: List[Citation] = Field(default=[], description="Sources used in the response")
    retrieved_contexts: List[RetrievedContext] = Field(default=[], description="Full context snippets retrieved")
    execution_time: float = Field(..., description="Time taken to process the request in seconds")
    success: bool = Field(True, description="Whether the request was processed successfully")