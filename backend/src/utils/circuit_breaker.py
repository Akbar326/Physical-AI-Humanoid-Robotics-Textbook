"""
Circuit breaker implementation for the RAG Agent API
"""

import time
import logging
from enum import Enum
from typing import Callable, Any, Optional, Type
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """
    Circuit breaker states
    """
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Tripped, blocking calls
    HALF_OPEN = "half_open"  # Testing if service is recovered


class CircuitBreaker:
    """
    Circuit breaker implementation to prevent cascading failures
    """

    def __init__(self,
                 failure_threshold: int = 5,
                 timeout: int = 60,
                 expected_exception: Type[Exception] = Exception):
        self.failure_threshold = failure_threshold
        self.timeout = timeout  # seconds
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = CircuitState.CLOSED

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Call the function with circuit breaker protection
        """
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker transitioning to HALF_OPEN state")
            else:
                raise Exception("Circuit breaker is OPEN. Service call blocked.")

        if self.state in [CircuitState.CLOSED, CircuitState.HALF_OPEN]:
            try:
                result = func(*args, **kwargs)
                self._on_success()
                return result
            except self.expected_exception as e:
                self._on_failure()
                raise e

    def _on_success(self):
        """
        Handle successful operation
        """
        self.failure_count = 0
        self.last_failure_time = None
        if self.state != CircuitState.CLOSED:
            self.state = CircuitState.CLOSED
            logger.info("Circuit breaker transitioning to CLOSED state")

    def _on_failure(self):
        """
        Handle failed operation
        """
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker transitioning to OPEN state after {self.failure_count} failures")

    def _should_attempt_reset(self) -> bool:
        """
        Check if enough time has passed to attempt resetting the circuit
        """
        if self.last_failure_time is None:
            return True

        return datetime.now() - self.last_failure_time >= timedelta(seconds=self.timeout)

    def reset(self):
        """
        Manually reset the circuit breaker
        """
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        logger.info("Circuit breaker manually reset to CLOSED state")

    def get_status(self) -> dict:
        """
        Get current status of the circuit breaker
        """
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "failure_threshold": self.failure_threshold,
            "timeout": self.timeout,
            "last_failure_time": self.last_failure_time.isoformat() if self.last_failure_time else None,
            "should_attempt_reset": self._should_attempt_reset() if self.state == CircuitState.OPEN else None
        }


class QdrantCircuitBreaker:
    """
    Specialized circuit breaker for Qdrant service calls
    """

    def __init__(self):
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            timeout=120,  # 2 minutes timeout
            expected_exception=Exception  # Catch all exceptions for Qdrant
        )

    def execute_qdrant_call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a Qdrant service call with circuit breaker protection
        """
        return self.circuit_breaker.call(func, *args, **kwargs)

    def get_status(self) -> dict:
        """
        Get the status of the Qdrant circuit breaker
        """
        return self.circuit_breaker.get_status()

    def reset(self):
        """
        Reset the Qdrant circuit breaker
        """
        self.circuit_breaker.reset()


# Global instance for convenience
qdrant_circuit_breaker = QdrantCircuitBreaker()