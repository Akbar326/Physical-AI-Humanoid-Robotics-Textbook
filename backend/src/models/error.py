"""
Error response models for the RAG Agent API
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ErrorResponse(BaseModel):
    """
    Model for error responses from the API
    """
    success: bool = Field(default=False, description="Indicates if the request was successful")
    error: str = Field(..., description="Error message")
    message: str = Field(..., description="Detailed error message")
    error_code: Optional[str] = Field(default=None, description="Specific error code")
    timestamp: Optional[str] = Field(default=None, description="Timestamp of the error")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")


class ValidationErrorResponse(ErrorResponse):
    """
    Model for validation error responses
    """
    error_code: str = Field(default="VALIDATION_ERROR", description="Validation error code")
    field_errors: Optional[Dict[str, str]] = Field(default=None, description="Field-specific validation errors")


class ServiceUnavailableErrorResponse(ErrorResponse):
    """
    Model for service unavailable error responses
    """
    error_code: str = Field(default="SERVICE_UNAVAILABLE", description="Service unavailable error code")
    retry_after: Optional[int] = Field(default=None, description="Suggested retry delay in seconds")


class RateLimitErrorResponse(ErrorResponse):
    """
    Model for rate limit error responses
    """
    error_code: str = Field(default="RATE_LIMIT_EXCEEDED", description="Rate limit error code")
    retry_after: Optional[int] = Field(default=None, description="Suggested retry delay in seconds")
    limit: Optional[int] = Field(default=None, description="Rate limit threshold")
    remaining: Optional[int] = Field(default=None, description="Remaining requests in current window")