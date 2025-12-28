"""
Query validation service for the RAG Agent API
"""

import re
import logging
from typing import Union
from ..models.query import QueryRequest
from .error_handler import QueryValidationError


logger = logging.getLogger(__name__)


class QueryValidationService:
    """
    Service for validating query requests and parameters
    """

    @staticmethod
    def validate_query_text(query_text: str) -> bool:
        """
        Validate the query text for appropriate content and format
        """
        if not query_text or not isinstance(query_text, str):
            raise QueryValidationError("Query text is required and must be a string")

        if len(query_text.strip()) == 0:
            raise QueryValidationError("Query text cannot be empty or just whitespace")

        if len(query_text) > 1000:
            raise QueryValidationError("Query must be between 1 and 1000 characters")

        # Check for potentially malicious patterns (basic injection prevention)
        malicious_patterns = [
            r"(?i)(drop\s+table|delete\s+from|update\s+\w+\s+set)",
            r"(?i)(exec\s*\(|execute\s*\(|sp_)",
            r"(?i)(union\s+select|insert\s+into)",
            r"(?i)(--|;|\*\/|\/\*)"
        ]

        for pattern in malicious_patterns:
            if re.search(pattern, query_text):
                raise QueryValidationError("Query contains potentially malicious content")

        return True

    @staticmethod
    def validate_max_results(max_results: int) -> bool:
        """
        Validate the max_results parameter
        """
        if not isinstance(max_results, int):
            raise QueryValidationError("max_results must be an integer")

        if not (1 <= max_results <= 20):
            raise QueryValidationError("max_results must be between 1 and 20")

        return True

    @staticmethod
    def validate_temperature(temperature: float) -> bool:
        """
        Validate the temperature parameter
        """
        if not isinstance(temperature, (int, float)):
            raise QueryValidationError("temperature must be a number")

        if not (0.0 <= float(temperature) <= 1.0):
            raise QueryValidationError("temperature must be between 0.0 and 1.0")

        return True

    @staticmethod
    def validate_include_citations(include_citations: bool) -> bool:
        """
        Validate the include_citations parameter
        """
        if not isinstance(include_citations, bool):
            raise QueryValidationError("include_citations must be a boolean")

        return True

    def validate_query_request(self, query_request: QueryRequest) -> bool:
        """
        Validate a complete QueryRequest object
        """
        try:
            # Validate query text
            self.validate_query_text(query_request.query)

            # Validate max_results
            self.validate_max_results(query_request.max_results)

            # Validate temperature
            self.validate_temperature(query_request.temperature)

            # Validate include_citations
            self.validate_include_citations(query_request.include_citations)

            logger.info("Query request validation passed")
            return True

        except QueryValidationError as e:
            logger.error(f"Query validation failed: {e.message}")
            raise

    def sanitize_query(self, query_text: str) -> str:
        """
        Sanitize the query text to remove potentially harmful content
        """
        # Remove potential SQL injection patterns
        sanitized = re.sub(r"(?i)(drop\s+table|delete\s+from|update\s+\w+\s+set)", "", query_text)
        sanitized = re.sub(r"(?i)(exec\s*\(|execute\s*\(|sp_)", "", sanitized)
        sanitized = re.sub(r"(?i)(union\s+select|insert\s+into)", "", sanitized)

        # Remove comment patterns
        sanitized = re.sub(r"(--|;|\*\/|\/\*)", "", sanitized)

        return sanitized.strip()

    @staticmethod
    def validate_input_parameters(query_request: QueryRequest) -> bool:
        """
        Validate all input parameters for potential security issues
        """
        # Validate query parameter
        if not query_request.query or not isinstance(query_request.query, str):
            raise QueryValidationError("Query parameter is required and must be a string")

        if len(query_request.query.strip()) == 0:
            raise QueryValidationError("Query parameter cannot be empty")

        if len(query_request.query) > 1000:
            raise QueryValidationError("Query parameter exceeds maximum length of 1000 characters")

        # Validate max_results parameter
        if not isinstance(query_request.max_results, int):
            raise QueryValidationError("max_results parameter must be an integer")

        if not (1 <= query_request.max_results <= 20):
            raise QueryValidationError("max_results parameter must be between 1 and 20")

        # Validate temperature parameter
        if not isinstance(query_request.temperature, (int, float)):
            raise QueryValidationError("temperature parameter must be a number")

        if not (0.0 <= query_request.temperature <= 1.0):
            raise QueryValidationError("temperature parameter must be between 0.0 and 1.0")

        # Validate include_citations parameter
        if not isinstance(query_request.include_citations, bool):
            raise QueryValidationError("include_citations parameter must be a boolean")

        return True


# Global instance for convenience
query_validation_service = QueryValidationService()