"""
Response formatter utility for the RAG Agent API
"""

import time
from typing import List
from ..models.query import QueryResponse, QueryRequest
from ..models.search import Citation, RetrievedContext


def format_response(
    query_request: QueryRequest,
    answer: str,
    retrieved_contexts: List[RetrievedContext],
    execution_time: float,
    success: bool = True
) -> QueryResponse:
    """
    Format the response with proper structure including citations and metadata
    """
    # Create citations from retrieved contexts
    citations = [
        Citation(
            url=ctx.url,
            title=ctx.title,
            score=ctx.score
        )
        for ctx in retrieved_contexts
    ]

    # Create the response object
    response = QueryResponse(
        query=query_request.query,
        answer=answer,
        citations=citations,
        retrieved_contexts=retrieved_contexts,
        execution_time=execution_time,
        success=success
    )

    return response


def format_error_response(
    original_query: str,
    error_message: str,
    execution_time: float,
    error_code: str = "INTERNAL_ERROR"
) -> QueryResponse:
    """
    Format an error response
    """
    response = QueryResponse(
        query=original_query,
        answer=f"Error processing query: {error_message}",
        citations=[],
        retrieved_contexts=[],
        execution_time=execution_time,
        success=False
    )

    return response


def extract_citations_from_answer(answer: str, retrieved_contexts: List[RetrievedContext]) -> List[Citation]:
    """
    Extract citations from the answer based on the retrieved contexts
    This is a simple implementation - in practice, you might use more sophisticated NLP techniques
    """
    citations = []
    answer_lower = answer.lower()

    for ctx in retrieved_contexts:
        # Check if content from this context appears in the answer
        if ctx.title.lower() in answer_lower or ctx.content[:50].lower() in answer_lower:
            citations.append(Citation(
                url=ctx.url,
                title=ctx.title,
                score=ctx.score
            ))

    return citations