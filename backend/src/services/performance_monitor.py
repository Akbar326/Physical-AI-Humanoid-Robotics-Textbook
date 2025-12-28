"""
Performance monitoring service for tracking and measuring response times
"""

from typing import Dict, Any, List, Optional
import time
import statistics
import logging
from datetime import datetime
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetric:
    """Data class for storing performance metrics"""
    operation: str
    response_time: float
    timestamp: datetime
    success: bool
    details: Optional[Dict[str, Any]] = None


class PerformanceMonitor:
    """Service for monitoring and tracking performance metrics"""

    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.operation_times: Dict[str, List[float]] = {}

    def start_timer(self) -> float:
        """Start a timer and return the start time"""
        return time.time()

    def end_timer(self, start_time: float, operation: str, success: bool = True, details: Optional[Dict[str, Any]] = None) -> float:
        """
        End a timer and record the response time

        Args:
            start_time: The time when the timer started
            operation: Name of the operation being timed
            success: Whether the operation was successful
            details: Additional details about the operation

        Returns:
            The response time in seconds
        """
        end_time = time.time()
        response_time = end_time - start_time

        # Record the metric
        metric = PerformanceMetric(
            operation=operation,
            response_time=response_time,
            timestamp=datetime.now(),
            success=success,
            details=details
        )
        self.metrics.append(metric)

        # Store response time by operation
        if operation not in self.operation_times:
            self.operation_times[operation] = []
        self.operation_times[operation].append(response_time)

        logger.debug(f"Operation '{operation}' took {response_time:.4f}s - Success: {success}")

        return response_time

    def measure_operation(self, operation: str, func, *args, **kwargs) -> Any:
        """
        Measure the execution time of a function

        Args:
            operation: Name of the operation being measured
            func: Function to execute and measure
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            The result of the function execution
        """
        start_time = self.start_timer()
        try:
            result = func(*args, **kwargs)
            self.end_timer(start_time, operation, success=True)
            return result
        except Exception as e:
            self.end_timer(start_time, operation, success=False, details={'error': str(e)})
            raise

    def get_response_time_stats(self, operation: str = None) -> Dict[str, Any]:
        """
        Get response time statistics for an operation or all operations

        Args:
            operation: Specific operation to get stats for, or None for all operations

        Returns:
            Dictionary with response time statistics
        """
        if operation:
            times = self.operation_times.get(operation, [])
        else:
            # Combine all operation times
            times = []
            for op_times in self.operation_times.values():
                times.extend(op_times)

        if not times:
            return {
                'operation': operation,
                'count': 0,
                'average': 0.0,
                'median': 0.0,
                'min': 0.0,
                'max': 0.0,
                'std_dev': 0.0,
                'p95': 0.0,
                'p99': 0.0
            }

        sorted_times = sorted(times)
        n = len(sorted_times)

        stats = {
            'operation': operation,
            'count': n,
            'average': statistics.mean(times),
            'median': statistics.median(times) if n > 0 else 0.0,
            'min': min(times),
            'max': max(times),
            'std_dev': statistics.stdev(times) if n > 1 else 0.0,
            'p95': sorted_times[int(0.95 * n)] if n > 0 else 0.0,
            'p99': sorted_times[int(0.99 * n)] if n > 0 else 0.0
        }

        return stats

    def get_success_rate(self, operation: str = None) -> float:
        """
        Get the success rate for an operation or all operations

        Args:
            operation: Specific operation to get success rate for, or None for all operations

        Returns:
            Success rate as a float between 0 and 1
        """
        if operation:
            relevant_metrics = [m for m in self.metrics if m.operation == operation]
        else:
            relevant_metrics = self.metrics

        if not relevant_metrics:
            return 0.0

        successful_count = sum(1 for m in relevant_metrics if m.success)
        return successful_count / len(relevant_metrics)

    def get_throughput(self, operation: str = None, time_window_minutes: int = 1) -> float:
        """
        Get the throughput (operations per minute) for an operation or all operations

        Args:
            operation: Specific operation to get throughput for, or None for all operations
            time_window_minutes: Time window in minutes to calculate throughput

        Returns:
            Throughput as operations per minute
        """
        time_threshold = datetime.now().timestamp() - (time_window_minutes * 60)

        if operation:
            relevant_metrics = [
                m for m in self.metrics
                if m.operation == operation and m.timestamp.timestamp() >= time_threshold
            ]
        else:
            relevant_metrics = [
                m for m in self.metrics
                if m.timestamp.timestamp() >= time_threshold
            ]

        if time_window_minutes <= 0:
            return 0.0

        return len(relevant_metrics) / time_window_minutes

    def get_all_operations(self) -> List[str]:
        """Get list of all operations that have been tracked"""
        return list(self.operation_times.keys())

    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all performance metrics

        Returns:
            Dictionary with performance summary
        """
        operations = self.get_all_operations()
        summary = {
            'total_operations': len(self.metrics),
            'time_period': {
                'start': min((m.timestamp for m in self.metrics), default=None),
                'end': max((m.timestamp for m in self.metrics), default=None)
            },
            'operations_summary': {}
        }

        for operation in operations:
            summary['operations_summary'][operation] = {
                'response_time_stats': self.get_response_time_stats(operation),
                'success_rate': self.get_success_rate(operation),
                'throughput_per_minute': self.get_throughput(operation)
            }

        return summary

    def clear_metrics(self):
        """Clear all stored metrics"""
        self.metrics.clear()
        self.operation_times.clear()

    def get_slow_operations(self, operation: str = None, threshold: float = 1.0) -> List[PerformanceMetric]:
        """
        Get operations that took longer than the specified threshold

        Args:
            operation: Specific operation to filter for, or None for all operations
            threshold: Response time threshold in seconds

        Returns:
            List of slow operations
        """
        if operation:
            relevant_metrics = [m for m in self.metrics if m.operation == operation]
        else:
            relevant_metrics = self.metrics

        return [m for m in relevant_metrics if m.response_time > threshold]

    def export_metrics(self) -> List[Dict[str, Any]]:
        """
        Export all metrics in a serializable format

        Returns:
            List of metrics in dictionary format
        """
        return [
            {
                'operation': m.operation,
                'response_time': m.response_time,
                'timestamp': m.timestamp.isoformat(),
                'success': m.success,
                'details': m.details
            }
            for m in self.metrics
        ]

    def get_trend_analysis(self, operation: str, window_size: int = 10) -> Dict[str, Any]:
        """
        Get trend analysis for an operation (comparing recent performance to historical)

        Args:
            operation: Operation to analyze
            window_size: Number of recent operations to compare

        Returns:
            Dictionary with trend analysis
        """
        if operation not in self.operation_times:
            return {}

        all_times = self.operation_times[operation]
        if len(all_times) < window_size * 2:
            # Not enough data for trend analysis
            return {'message': 'Not enough data for trend analysis'}

        recent_times = all_times[-window_size:]
        historical_times = all_times[-(window_size * 2):-window_size]

        if not historical_times:
            return {'message': 'Not enough historical data for comparison'}

        recent_avg = statistics.mean(recent_times)
        historical_avg = statistics.mean(historical_times)

        trend = "improving" if recent_avg < historical_avg else "degrading" if recent_avg > historical_avg else "stable"

        return {
            'trend': trend,
            'recent_average': recent_avg,
            'historical_average': historical_avg,
            'change_percentage': ((recent_avg - historical_avg) / historical_avg) * 100 if historical_avg != 0 else 0
        }


class PerformanceDecorator:
    """Decorator for easily measuring performance of functions"""

    def __init__(self, monitor: PerformanceMonitor, operation_name: str):
        self.monitor = monitor
        self.operation_name = operation_name

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            return self.monitor.measure_operation(self.operation_name, func, *args, **kwargs)
        return wrapper