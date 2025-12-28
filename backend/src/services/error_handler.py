"""
Error handlers for the RAG Agent API
"""

import logging
from typing import Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


logger = logging.getLogger(__name__)


class RAGAgentError(Exception):
    """
    Base exception class for RAG Agent API errors
    """
    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR", status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class QueryValidationError(RAGAgentError):
    """
    Exception raised for query validation errors
    """
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR", 422)


class RetrievalError(RAGAgentError):
    """
    Exception raised for retrieval errors
    """
    def __init__(self, message: str):
        super().__init__(message, "RETRIEVAL_ERROR", 500)


class AgentProcessingError(RAGAgentError):
    """
    Exception raised for agent processing errors
    """
    def __init__(self, message: str):
        super().__init__(message, "AGENT_ERROR", 500)


class ServiceUnavailableError(RAGAgentError):
    """
    Exception raised when a required service is unavailable
    """
    def __init__(self, message: str):
        super().__init__(message, "SERVICE_UNAVAILABLE", 503)


async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    Handle validation errors
    """
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Request validation failed",
            "error_code": "VALIDATION_ERROR",
            "success": False
        }
    )


async def rag_agent_exception_handler(request: Request, exc: RAGAgentError):
    """
    Handle custom RAG agent errors
    """
    logger.error(f"RAG Agent error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error_code": exc.error_code,
            "success": False
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions
    """
    logger.error(f"General error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred",
            "error_code": "INTERNAL_ERROR",
            "success": False
        }
    )


def setup_error_handlers(app):
    """
    Register error handlers with the FastAPI app
    """
    app.exception_handler(ValidationError)(validation_exception_handler)
    app.exception_handler(RAGAgentError)(rag_agent_exception_handler)
    app.exception_handler(Exception)(general_exception_handler)