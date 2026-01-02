"""
Rate limiting middleware for the RAG Agent API
"""

import time
import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from ..utils.rate_limiter import api_rate_limiter


logger = logging.getLogger(__name__)


async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware to enforce rate limiting on API requests
    """
    # Use client IP as the identifier for rate limiting
    client_ip = request.client.host if request.client else "unknown"

    # Check if the request is allowed based on rate limits
    if not api_rate_limiter.is_allowed(client_ip):
        # Get rate limit headers for response
        headers = api_rate_limiter.get_rate_limit_headers(client_ip)

        logger.warning(f"Rate limit exceeded for IP: {client_ip}")

        # Return 429 (Too Many Requests) response
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Rate limit exceeded. Please try again later.",
                "error_code": "RATE_LIMIT_EXCEEDED",
                "success": False
            },
            headers={
                "X-RateLimit-Limit": headers["X-RateLimit-Limit"],
                "X-RateLimit-Remaining": headers["X-RateLimit-Remaining"],
                "X-RateLimit-Reset": headers["X-RateLimit-Reset"],
                "Retry-After": headers["Retry-After"]
            }
        )

    # Add rate limit headers to the response
    response = await call_next(request)

    # Get current rate limit status
    headers = api_rate_limiter.get_rate_limit_headers(client_ip)

    # Add rate limit headers to response
    response.headers["X-RateLimit-Limit"] = headers["X-RateLimit-Limit"]
    response.headers["X-RateLimit-Remaining"] = headers["X-RateLimit-Remaining"]
    response.headers["X-RateLimit-Reset"] = headers["X-RateLimit-Reset"]

    return response