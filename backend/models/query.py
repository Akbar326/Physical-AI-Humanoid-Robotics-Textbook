from pydantic import BaseModel
from typing import List, Optional
from .document import Document


class QueryRequest(BaseModel):
    """
    Represents a user query to the RAG system.
    """
    query: str
    session_id: Optional[str] = None
    top_k: int = 5


class SourceDocument(BaseModel):
    """
    Represents a source document used in the response.
    """
    title: str
    url: str
    content: str


class QueryResponse(BaseModel):
    """
    Represents the response from the RAG system to a user query.
    """
    answer: str
    sources: List[SourceDocument]
    query_time: float
    session_id: Optional[str] = None


class IngestRequest(BaseModel):
    """
    Request model for ingestion endpoint.
    """
    sitemap_url: str
    force_rebuild: bool = False