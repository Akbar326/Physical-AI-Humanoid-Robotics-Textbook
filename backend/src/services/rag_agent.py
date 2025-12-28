"""
RAG agent service for the RAG Agent API
"""

import time
import logging
from typing import List
from ..models.query import QueryRequest
from ..models.search import RetrievedContext
from ..models.agent import AgentContext
from .qdrant_search import qdrant_search_service
from .openai_agent import openai_agent_service
from ..utils.response_formatter import format_response, format_error_response
from ..utils.performance_monitor import performance_monitor
from .response_validation import response_validation_service
from .query_analyzer import query_analyzer_service, QueryType
from .query_handlers import (
    factual_query_handler,
    analytical_query_handler,
    comparative_query_handler
)


logger = logging.getLogger(__name__)


class RAGAgentService:
    """
    Main RAG agent service that coordinates search and generation
    """

    def __init__(self):
        self.qdrant_service = qdrant_search_service
        self.openai_service = openai_agent_service

    def process_query(self, query_request: QueryRequest) -> str:
        """
        Process a query request through the full RAG pipeline
        """
        start_time = time.time()

        try:
            logger.info(f"Processing query: {query_request.query[:50]}...")

            # Step 1: Analyze query type
            query_analysis = query_analyzer_service.analyze_query(query_request.query)
            logger.info(f"Query type detected: {query_analysis.query_type.value} (confidence: {query_analysis.confidence:.2f})")

            # Step 2: Search for relevant content in Qdrant
            retrieved_contexts = self.qdrant_service.search_by_text(
                query_request.query,
                query_request.max_results
            )

            logger.info(f"Retrieved {len(retrieved_contexts)} context chunks")

            # Step 3: Generate response using appropriate handler based on query type
            if query_analysis.query_type == QueryType.FACTUAL:
                answer = factual_query_handler.process_factual_query(
                    query_request.query,
                    retrieved_contexts,
                    query_request.temperature
                )
            elif query_analysis.query_type == QueryType.ANALYTICAL:
                answer = analytical_query_handler.process_analytical_query(
                    query_request.query,
                    retrieved_contexts,
                    query_request.temperature
                )
            elif query_analysis.query_type == QueryType.COMPARATIVE:
                answer = comparative_query_handler.process_comparative_query(
                    query_request.query,
                    retrieved_contexts,
                    query_request.temperature
                )
            else:
                # Default to standard processing for unknown query types
                answer = self.openai_service.process_query(
                    query_request.query,
                    retrieved_contexts,
                    query_request.temperature
                )

            execution_time = time.time() - start_time

            logger.info(f"Query processed successfully in {execution_time:.2f}s")
            return answer

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Error processing query: {str(e)}", exc_info=True)
            raise e

    def process_query_with_full_response(self, query_request: QueryRequest):
        """
        Process a query and return a complete response with metadata
        """
        start_time = performance_monitor.start_timer()
        request_id = f"rag_query_{start_time}"

        try:
            logger.info(f"Processing query with full response: {query_request.query[:50]}...")

            # Step 1: Search for relevant content in Qdrant
            retrieved_contexts = self.qdrant_service.search_by_text(
                query_request.query,
                query_request.max_results
            )

            logger.info(f"Retrieved {len(retrieved_contexts)} context chunks")

            # Step 2: Generate response using OpenAI agent with retrieved context
            answer = self.openai_service.process_query(
                query_request.query,
                retrieved_contexts,
                query_request.temperature
            )

            execution_time = time.time() - start_time

            # Step 3: Format the response
            response = format_response(
                query_request=query_request,
                answer=answer,
                retrieved_contexts=retrieved_contexts,
                execution_time=execution_time,
                success=True
            )

            # Validate response grounding
            validation_report = response_validation_service.validate_response_quality(response)
            logger.info(f"Response validation report: {validation_report}")

            # Record performance metric
            performance_monitor.record_metric(
                request_id=request_id,
                start_time=start_time,
                endpoint="/api/v1/query",
                success=True,
                query_length=len(query_request.query),
                retrieved_contexts_count=len(retrieved_contexts)
            )

            logger.info(f"Full response formatted successfully in {execution_time:.2f}s")
            return response

        except Exception as e:
            execution_time = time.time() - start_time

            # Record performance metric for failed request
            performance_monitor.record_metric(
                request_id=request_id,
                start_time=start_time,
                endpoint="/api/v1/query",
                success=False,
                status_code=500,
                query_length=len(query_request.query)
            )

            logger.error(f"Error in full response processing: {str(e)}", exc_info=True)

            # Format error response
            error_response = format_error_response(
                original_query=query_request.query,
                error_message=str(e),
                execution_time=execution_time
            )

            return error_response

    def validate_query_request(self, query_request: QueryRequest) -> bool:
        """
        Validate the query request parameters
        """
        # Check query length
        if not (1 <= len(query_request.query) <= 1000):
            raise ValueError("Query must be between 1 and 1000 characters")

        # Check max_results range
        if not (1 <= query_request.max_results <= 20):
            raise ValueError("max_results must be between 1 and 20")

        # Check temperature range
        if not (0.0 <= query_request.temperature <= 1.0):
            raise ValueError("temperature must be between 0.0 and 1.0")

        return True


# Global instance for convenience
rag_agent_service = RAGAgentService()