"""
Query API endpoint for the RAG Agent API
"""

import time
import logging
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from ...models.query import QueryRequest, QueryResponse
from ...services.rag_agent import rag_agent_service
from ...services.validation import query_validation_service
from ...services.error_handler import QueryValidationError, RetrievalError, AgentProcessingError
from ...utils.performance_monitor import performance_monitor


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/query", summary="Query RAG Agent", response_model=QueryResponse)
async def query_rag_agent(query_request: QueryRequest) -> QueryResponse:
    """
    Submit a natural language query to the RAG agent, which will retrieve relevant
    book content and generate a response grounded in that context.
    """
    start_time = performance_monitor.start_timer()
    request_id = f"api_query_{start_time}"
    logger.info(f"Received query request: {query_request.query[:50]}...")

    try:
        # Validate the query request
        query_validation_service.validate_query_request(query_request)
        logger.info("Query request validation passed")

        # Process the query through the RAG pipeline
        response = rag_agent_service.process_query_with_full_response(query_request)

        # Calculate total execution time
        execution_time = time.time() - start_time
        logger.info(f"Query processed successfully in {execution_time:.2f}s")

        # Update execution time in response
        response.execution_time = execution_time

        # Record performance metric
        performance_monitor.record_metric(
            request_id=request_id,
            start_time=start_time,
            endpoint="/api/v1/query",
            success=True,
            status_code=200,
            query_length=len(query_request.query),
            retrieved_contexts_count=len(response.retrieved_contexts)
        )

        return response

    except QueryValidationError as e:
        execution_time = time.time() - start_time
        logger.error(f"Query validation error: {e.message}")

        # Record performance metric for failed request
        performance_monitor.record_metric(
            request_id=request_id,
            start_time=start_time,
            endpoint="/api/v1/query",
            success=False,
            status_code=422,
            query_length=len(query_request.query)
        )

        raise HTTPException(
            status_code=422,
            detail={
                "error": "Query validation failed",
                "message": e.message,
                "success": False
            }
        )

    except RetrievalError as e:
        execution_time = time.time() - start_time
        logger.error(f"Retrieval error: {e.message}")

        # Record performance metric for failed request
        performance_monitor.record_metric(
            request_id=request_id,
            start_time=start_time,
            endpoint="/api/v1/query",
            success=False,
            status_code=500,
            query_length=len(query_request.query)
        )

        raise HTTPException(
            status_code=500,
            detail={
                "error": "Content retrieval failed",
                "message": e.message,
                "success": False
            }
        )

    except AgentProcessingError as e:
        execution_time = time.time() - start_time
        logger.error(f"Agent processing error: {e.message}")

        # Record performance metric for failed request
        performance_monitor.record_metric(
            request_id=request_id,
            start_time=start_time,
            endpoint="/api/v1/query",
            success=False,
            status_code=500,
            query_length=len(query_request.query)
        )

        raise HTTPException(
            status_code=500,
            detail={
                "error": "Agent processing failed",
                "message": e.message,
                "success": False
            }
        )

    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Unexpected error processing query: {str(e)}", exc_info=True)

        # Record performance metric for failed request
        performance_monitor.record_metric(
            request_id=request_id,
            start_time=start_time,
            endpoint="/api/v1/query",
            success=False,
            status_code=500,
            query_length=len(query_request.query)
        )

        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": "An unexpected error occurred while processing your query",
                "success": False
            }
        )