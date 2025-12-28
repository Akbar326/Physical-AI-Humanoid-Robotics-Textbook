"""
Response validation service for the RAG Agent API
"""

import logging
from typing import List
from ..models.query import QueryResponse
from ..models.search import RetrievedContext


logger = logging.getLogger(__name__)


class ResponseValidationService:
    """
    Service for validating that responses are properly grounded in retrieved context
    """

    @staticmethod
    def validate_response_grounding(query: str, answer: str, retrieved_contexts: List[RetrievedContext]) -> bool:
        """
        Validate that the response is grounded in the retrieved contexts
        """
        if not retrieved_contexts:
            # If no contexts were retrieved, the answer should indicate this
            no_content_indicators = [
                "no relevant", "not found", "no information", "not available",
                "no context", "not mentioned", "not provided"
            ]
            return any(indicator in answer.lower() for indicator in no_content_indicators)

        # Check if the answer contains information from the retrieved contexts
        answer_lower = answer.lower()

        # Look for evidence that the answer is based on the retrieved content
        grounding_evidence = 0
        total_contexts = len(retrieved_contexts)

        for ctx in retrieved_contexts:
            ctx_content_lower = ctx.content.lower()
            ctx_title_lower = ctx.title.lower()

            # Check if parts of the context appear in the answer
            if any(word in answer_lower for word in ctx_content_lower.split()[:20] if len(word) > 3):  # Check first 20 words
                grounding_evidence += 1
            elif ctx_title_lower in answer_lower:
                grounding_evidence += 1
            elif any(keyword in answer_lower for keyword in ctx_content_lower[:200].split() if len(keyword) > 5):  # Check first 200 chars
                grounding_evidence += 1

        # Consider it grounded if at least one context contributed to the answer
        is_qualified = grounding_evidence > 0
        logger.info(f"Response grounding validation: {grounding_evidence}/{total_contexts} contexts found in answer")

        return is_qualified

    @staticmethod
    def validate_citations_consistency(response: QueryResponse) -> bool:
        """
        Validate that citations in the response are consistent with retrieved contexts
        """
        if not response.citations or not response.retrieved_contexts:
            return len(response.citations) == 0 and len(response.retrieved_contexts) == 0

        # Check if each citation corresponds to a retrieved context
        citation_urls = {cit.url for cit in response.citations}
        context_urls = {ctx.url for ctx in response.retrieved_contexts}

        # All citations should come from retrieved contexts
        return citation_urls.issubset(context_urls)

    @staticmethod
    def validate_response_quality(response: QueryResponse) -> dict:
        """
        Validate overall response quality and return a validation report
        """
        validation_report = {
            "grounding_valid": False,
            "citations_valid": False,
            "response_complete": False,
            "quality_score": 0.0
        }

        # Validate grounding
        validation_report["grounding_valid"] = ResponseValidationService.validate_response_grounding(
            response.query,
            response.answer,
            response.retrieved_contexts
        )

        # Validate citations
        validation_report["citations_valid"] = ResponseValidationService.validate_citations_consistency(response)

        # Check if response is complete (not empty)
        validation_report["response_complete"] = bool(response.answer and response.answer.strip())

        # Calculate quality score
        quality_points = sum([
            1 if validation_report["grounding_valid"] else 0,
            1 if validation_report["citations_valid"] else 0,
            1 if validation_report["response_complete"] else 0
        ])
        validation_report["quality_score"] = quality_points / 3.0

        logger.info(f"Response quality validation score: {validation_report['quality_score']:.2f}")
        return validation_report

    @staticmethod
    def validate_response_time(response: QueryResponse, max_time: float = 5.0) -> bool:
        """
        Validate that response time is within acceptable limits
        """
        is_acceptable = response.execution_time <= max_time
        logger.info(f"Response time validation: {response.execution_time:.2f}s <= {max_time}s = {is_acceptable}")
        return is_acceptable


# Global instance for convenience
response_validation_service = ResponseValidationService()