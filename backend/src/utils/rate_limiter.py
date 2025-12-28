"""
Rate limiting utility for the RAG Agent API
"""

import time
import logging
from typing import Dict, Optional
from collections import defaultdict, deque
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple rate limiter to control API request frequency
    """

    def __init__(self, max_requests: int = 100, time_window: int = 60):
        """
        Initialize rate limiter

        Args:
            max_requests: Maximum number of requests allowed in the time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, deque] = defaultdict(deque)  # Store request timestamps by key

    def is_allowed(self, key: str) -> bool:
        """
        Check if a request is allowed for the given key

        Args:
            key: Unique identifier for the requester (e.g., IP address)

        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        # Clean old requests outside the time window
        while self.requests[key] and self.requests[key][0] <= now - self.time_window:
            self.requests[key].popleft()

        # Check if we're under the limit
        if len(self.requests[key]) < self.max_requests:
            self.requests[key].append(now)
            return True
        else:
            return False

    def get_remaining_requests(self, key: str) -> int:
        """
        Get the number of remaining requests for the given key

        Args:
            key: Unique identifier for the requester

        Returns:
            Number of remaining requests
        """
        now = time.time()
        # Clean old requests outside the time window
        while self.requests[key] and self.requests[key][0] <= now - self.time_window:
            self.requests[key].popleft()

        return max(0, self.max_requests - len(self.requests[key]))

    def get_reset_time(self, key: str) -> float:
        """
        Get the time when the rate limit will reset for the given key

        Args:
            key: Unique identifier for the requester

        Returns:
            Unix timestamp when the rate limit will reset
        """
        if not self.requests[key]:
            return time.time()

        # Reset time is the time of the oldest request + time_window
        oldest_request = self.requests[key][0]
        return oldest_request + self.time_window

    def get_status(self, key: str) -> dict:
        """
        Get the rate limiting status for the given key

        Args:
            key: Unique identifier for the requester

        Returns:
            Status information including remaining requests and reset time
        """
        return {
            "limit": self.max_requests,
            "remaining": self.get_remaining_requests(key),
            "reset_time": self.get_reset_time(key),
            "window": self.time_window
        }


class APIRateLimiter:
    """
    API-specific rate limiter
    """

    def __init__(self, max_requests_per_minute: int = 100):
        self.rate_limiter = RateLimiter(max_requests=max_requests_per_minute, time_window=60)
        self.max_requests_per_minute = max_requests_per_minute

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request is allowed for the given identifier

        Args:
            identifier: Request identifier (e.g., IP address, user ID)

        Returns:
            True if request is allowed, False otherwise
        """
        return self.rate_limiter.is_allowed(identifier)

    def get_rate_limit_headers(self, identifier: str) -> dict:
        """
        Get rate limit headers for response

        Args:
            identifier: Request identifier

        Returns:
            Dictionary of rate limit headers
        """
        status = self.rate_limiter.get_status(identifier)
        reset_time = int(status["reset_time"])
        current_time = int(time.time())

        return {
            "X-RateLimit-Limit": str(status["limit"]),
            "X-RateLimit-Remaining": str(status["remaining"]),
            "X-RateLimit-Reset": str(reset_time),
            "Retry-After": str(max(0, reset_time - current_time))
        }

    def get_status(self, identifier: str) -> dict:
        """
        Get rate limiting status for the given identifier
        """
        return self.rate_limiter.get_status(identifier)


# Global instance for convenience
api_rate_limiter = APIRateLimiter(max_requests_per_minute=100)