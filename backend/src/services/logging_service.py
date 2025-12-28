"""
Logging and monitoring service for validation processes
"""

from typing import Dict, Any, Optional
import logging
import sys
from datetime import datetime
from enum import Enum
import json
import time
from dataclasses import dataclass


class ValidationLogLevel(Enum):
    """Enumeration for validation-specific log levels"""
    VALIDATION_START = "validation_start"
    VALIDATION_END = "validation_end"
    VALIDATION_STEP = "validation_step"
    VALIDATION_RESULT = "validation_result"
    PERFORMANCE_METRIC = "performance_metric"
    ERROR_OCCURRED = "error_occurred"
    WARNING_ISSUED = "warning_issued"


@dataclass
class ValidationLogEntry:
    """Data class for validation log entries"""
    level: ValidationLogLevel
    message: str
    timestamp: datetime
    duration: Optional[float] = None
    validation_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    success: Optional[bool] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class ValidationLoggingService:
    """Service for logging and monitoring validation processes"""

    def __init__(self, name: str = "validation_logger"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create a custom formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Create a handler that writes to stdout
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        # Add handler to logger if not already added
        if not self.logger.handlers:
            self.logger.addHandler(handler)

        # Store validation logs
        self.validation_logs: list = []

    def log_validation_start(self, validation_id: str, message: str = None, details: Dict[str, Any] = None):
        """Log the start of a validation process"""
        log_entry = ValidationLogEntry(
            level=ValidationLogLevel.VALIDATION_START,
            message=message or f"Starting validation: {validation_id}",
            timestamp=datetime.now(),
            validation_id=validation_id,
            details=details or {}
        )

        self.logger.info(f"[{validation_id}] {log_entry.message}")
        self.validation_logs.append(log_entry)

    def log_validation_end(self, validation_id: str, duration: float, success: bool,
                          message: str = None, details: Dict[str, Any] = None):
        """Log the end of a validation process"""
        log_entry = ValidationLogEntry(
            level=ValidationLogLevel.VALIDATION_END,
            message=message or f"Validation completed: {validation_id}",
            timestamp=datetime.now(),
            duration=duration,
            validation_id=validation_id,
            details=details or {},
            success=success
        )

        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"[{validation_id}] {log_entry.message} - {status} (Duration: {duration:.2f}s)")
        self.validation_logs.append(log_entry)

    def log_validation_step(self, validation_id: str, step: str, message: str = None,
                           details: Dict[str, Any] = None):
        """Log a step in the validation process"""
        log_entry = ValidationLogEntry(
            level=ValidationLogLevel.VALIDATION_STEP,
            message=message or f"Validation step: {step}",
            timestamp=datetime.now(),
            validation_id=validation_id,
            details=details or {}
        )

        self.logger.debug(f"[{validation_id}] Step: {step}")
        self.validation_logs.append(log_entry)

    def log_validation_result(self, validation_id: str, result: Any, success: bool,
                             message: str = None, details: Dict[str, Any] = None):
        """Log the result of a validation"""
        log_entry = ValidationLogEntry(
            level=ValidationLogLevel.VALIDATION_RESULT,
            message=message or f"Validation result: {success}",
            timestamp=datetime.now(),
            validation_id=validation_id,
            details=details or {},
            success=success
        )

        result_str = str(result)[:100] + "..." if len(str(result)) > 100 else str(result)
        self.logger.info(f"[{validation_id}] Result: {result_str} - Success: {success}")
        self.validation_logs.append(log_entry)

    def log_performance_metric(self, validation_id: str, metric_name: str, value: Any,
                              message: str = None, details: Dict[str, Any] = None):
        """Log a performance metric"""
        log_entry = ValidationLogEntry(
            level=ValidationLogLevel.PERFORMANCE_METRIC,
            message=message or f"Performance metric: {metric_name} = {value}",
            timestamp=datetime.now(),
            validation_id=validation_id,
            details=details or {}
        )

        self.logger.info(f"[{validation_id}] Metric: {metric_name} = {value}")
        self.validation_logs.append(log_entry)

    def log_error(self, validation_id: str, error: Exception, message: str = None,
                 details: Dict[str, Any] = None):
        """Log an error that occurred during validation"""
        log_entry = ValidationLogEntry(
            level=ValidationLogLevel.ERROR_OCCURRED,
            message=message or f"Error occurred: {str(error)}",
            timestamp=datetime.now(),
            validation_id=validation_id,
            details=details or {},
            success=False
        )

        self.logger.error(f"[{validation_id}] Error: {str(error)}", exc_info=True)
        self.validation_logs.append(log_entry)

    def log_warning(self, validation_id: str, message: str, details: Dict[str, Any] = None):
        """Log a warning during validation"""
        log_entry = ValidationLogEntry(
            level=ValidationLogLevel.WARNING_ISSUED,
            message=message,
            timestamp=datetime.now(),
            validation_id=validation_id,
            details=details or {},
            success=None
        )

        self.logger.warning(f"[{validation_id}] Warning: {message}")
        self.validation_logs.append(log_entry)

    def measure_and_log(self, validation_id: str, operation_name: str,
                       operation_func, *args, **kwargs) -> Any:
        """
        Execute an operation and measure its performance, logging the results

        Args:
            validation_id: ID of the validation process
            operation_name: Name of the operation being measured
            operation_func: Function to execute
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of the operation
        """
        start_time = time.time()
        self.log_validation_step(validation_id, f"start_{operation_name}",
                                f"Starting operation: {operation_name}")

        try:
            result = operation_func(*args, **kwargs)
            duration = time.time() - start_time

            self.log_performance_metric(validation_id, f"{operation_name}_duration", duration)
            self.log_validation_step(validation_id, f"end_{operation_name}",
                                   f"Completed operation: {operation_name}")

            return result
        except Exception as e:
            duration = time.time() - start_time
            self.log_performance_metric(validation_id, f"{operation_name}_duration", duration)
            self.log_error(validation_id, e, f"Operation failed: {operation_name}")
            raise

    def get_validation_summary(self, validation_id: str = None) -> Dict[str, Any]:
        """
        Get a summary of validation logs

        Args:
            validation_id: Optional ID to filter logs for a specific validation

        Returns:
            Dictionary with validation summary
        """
        if validation_id:
            logs = [log for log in self.validation_logs if log.validation_id == validation_id]
        else:
            logs = self.validation_logs

        summary = {
            'total_logs': len(logs),
            'logs_by_level': {},
            'success_count': 0,
            'error_count': 0,
            'warning_count': 0,
            'total_duration': 0.0
        }

        for log in logs:
            # Count by level
            level = log.level.value
            if level not in summary['logs_by_level']:
                summary['logs_by_level'][level] = 0
            summary['logs_by_level'][level] += 1

            # Count successes and errors
            if log.success is True:
                summary['success_count'] += 1
            elif log.success is False:
                summary['error_count'] += 1

            # Count warnings
            if log.level == ValidationLogLevel.WARNING_ISSUED:
                summary['warning_count'] += 1

            # Add duration if available
            if log.duration:
                summary['total_duration'] += log.duration

        return summary

    def export_logs(self, validation_id: str = None) -> list:
        """
        Export logs in a serializable format

        Args:
            validation_id: Optional ID to filter logs for a specific validation

        Returns:
            List of logs in dictionary format
        """
        if validation_id:
            logs = [log for log in self.validation_logs if log.validation_id == validation_id]
        else:
            logs = self.validation_logs

        return [
            {
                'level': log.level.value,
                'message': log.message,
                'timestamp': log.timestamp.isoformat(),
                'duration': log.duration,
                'validation_id': log.validation_id,
                'details': log.details,
                'success': log.success
            }
            for log in logs
        ]

    def clear_logs(self):
        """Clear all stored logs"""
        self.validation_logs.clear()

    def log_validation_with_context(self, validation_id: str,
                                   validation_func, *args, **kwargs) -> Any:
        """
        Execute a validation function with automatic logging of start, end, and errors

        Args:
            validation_id: ID for the validation process
            validation_func: Function to execute
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Result of the validation function
        """
        start_time = time.time()
        self.log_validation_start(validation_id, f"Starting validation function: {validation_func.__name__}")

        try:
            result = validation_func(*args, **kwargs)
            duration = time.time() - start_time

            self.log_validation_result(validation_id, result, True)
            self.log_validation_end(validation_id, duration, True)

            return result
        except Exception as e:
            duration = time.time() - start_time
            self.log_error(validation_id, e)
            self.log_validation_end(validation_id, duration, False)
            raise

    def log_metric_aggregation(self, validation_id: str, metric_name: str,
                              values: list, aggregation_type: str = "avg"):
        """
        Log aggregated metrics

        Args:
            validation_id: ID of the validation process
            metric_name: Name of the metric
            values: List of metric values to aggregate
            aggregation_type: Type of aggregation ('avg', 'sum', 'min', 'max', 'count')
        """
        if not values:
            return

        if aggregation_type == "avg":
            result = sum(values) / len(values)
        elif aggregation_type == "sum":
            result = sum(values)
        elif aggregation_type == "min":
            result = min(values)
        elif aggregation_type == "max":
            result = max(values)
        elif aggregation_type == "count":
            result = len(values)
        else:
            raise ValueError(f"Unknown aggregation type: {aggregation_type}")

        self.log_performance_metric(
            validation_id,
            f"{metric_name}_{aggregation_type}",
            result,
            details={"original_values": values, "count": len(values)}
        )


# Global validation logging service instance
global_validation_logger = ValidationLoggingService()


def get_validation_logger() -> ValidationLoggingService:
    """Get the global validation logging service instance"""
    return global_validation_logger