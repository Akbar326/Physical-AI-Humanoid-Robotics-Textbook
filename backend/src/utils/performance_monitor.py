"""
Performance monitoring utility for the RAG Agent API
"""

import time
import logging
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from threading import Lock


logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """
    Data class to store performance metrics
    """
    request_id: str
    start_time: float
    end_time: float
    duration: float
    endpoint: str
    status_code: int
    success: bool
    query_length: int = 0
    retrieved_contexts_count: int = 0


class PerformanceMonitor:
    """
    Performance monitoring service to track response times and other metrics
    """

    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.lock = Lock()
        self.max_metrics_to_store = 1000  # Keep last 1000 metrics in memory

    def start_timer(self) -> float:
        """
        Start a timer and return the start time
        """
        return time.time()

    def record_metric(
        self,
        request_id: str,
        start_time: float,
        endpoint: str,
        status_code: int = 200,
        success: bool = True,
        query_length: int = 0,
        retrieved_contexts_count: int = 0
    ) -> PerformanceMetric:
        """
        Record a performance metric
        """
        end_time = time.time()
        duration = end_time - start_time

        metric = PerformanceMetric(
            request_id=request_id,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            endpoint=endpoint,
            status_code=status_code,
            success=success,
            query_length=query_length,
            retrieved_contexts_count=retrieved_contexts_count
        )

        with self.lock:
            self.metrics.append(metric)

            # Keep only the most recent metrics
            if len(self.metrics) > self.max_metrics_to_store:
                self.metrics = self.metrics[-self.max_metrics_to_store:]

        logger.info(f"Performance metric recorded: {endpoint} took {duration:.2f}s")

        return metric

    def get_average_response_time(self, endpoint: Optional[str] = None,
                                 time_window_minutes: int = 60) -> float:
        """
        Get average response time for a specific endpoint or overall
        """
        cutoff_time = time.time() - (time_window_minutes * 60)

        with self.lock:
            recent_metrics = [
                m for m in self.metrics
                if m.end_time >= cutoff_time and (endpoint is None or m.endpoint == endpoint)
            ]

        if not recent_metrics:
            return 0.0

        total_duration = sum(m.duration for m in recent_metrics)
        return total_duration / len(recent_metrics)

    def get_p95_response_time(self, endpoint: Optional[str] = None,
                              time_window_minutes: int = 60) -> float:
        """
        Get 95th percentile response time for a specific endpoint or overall
        """
        cutoff_time = time.time() - (time_window_minutes * 60)

        with self.lock:
            recent_metrics = [
                m.duration for m in self.metrics
                if m.end_time >= cutoff_time and (endpoint is None or m.endpoint == endpoint)
            ]

        if not recent_metrics:
            return 0.0

        # Sort durations and calculate p95
        sorted_durations = sorted(recent_metrics)
        p95_index = int(0.95 * len(sorted_durations))

        return sorted_durations[min(p95_index, len(sorted_durations) - 1)]

    def get_success_rate(self, endpoint: Optional[str] = None,
                        time_window_minutes: int = 60) -> float:
        """
        Get success rate for a specific endpoint or overall
        """
        cutoff_time = time.time() - (time_window_minutes * 60)

        with self.lock:
            recent_metrics = [
                m for m in self.metrics
                if m.end_time >= cutoff_time and (endpoint is None or m.endpoint == endpoint)
            ]

        if not recent_metrics:
            return 0.0

        successful_requests = sum(1 for m in recent_metrics if m.success)
        return successful_requests / len(recent_metrics)

    def get_throughput(self, endpoint: Optional[str] = None,
                      time_window_minutes: int = 1) -> float:
        """
        Get requests per minute for a specific endpoint or overall
        """
        cutoff_time = time.time() - (time_window_minutes * 60)

        with self.lock:
            recent_metrics = [
                m for m in self.metrics
                if m.end_time >= cutoff_time and (endpoint is None or m.endpoint == endpoint)
            ]

        return len(recent_metrics) / time_window_minutes if time_window_minutes > 0 else 0.0

    def get_metrics_summary(self, endpoint: Optional[str] = None,
                          time_window_minutes: int = 60) -> Dict[str, float]:
        """
        Get a summary of performance metrics
        """
        return {
            "avg_response_time": self.get_average_response_time(endpoint, time_window_minutes),
            "p95_response_time": self.get_p95_response_time(endpoint, time_window_minutes),
            "success_rate": self.get_success_rate(endpoint, time_window_minutes),
            "throughput": self.get_throughput(endpoint, time_window_minutes),
            "time_window_minutes": time_window_minutes
        }


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def monitor_performance(endpoint: str):
    """
    Decorator to monitor performance of functions
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            start_time = performance_monitor.start_timer()
            request_id = f"{endpoint}_{start_time}"

            try:
                result = func(*args, **kwargs)
                performance_monitor.record_metric(
                    request_id=request_id,
                    start_time=start_time,
                    endpoint=endpoint,
                    success=True
                )
                return result
            except Exception as e:
                performance_monitor.record_metric(
                    request_id=request_id,
                    start_time=start_time,
                    endpoint=endpoint,
                    success=False,
                    status_code=500
                )
                raise e
        return wrapper
    return decorator