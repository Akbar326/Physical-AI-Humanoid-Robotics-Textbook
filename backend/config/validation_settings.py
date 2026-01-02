"""
Configuration options for validation parameters
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ValidationSettings:
    """Configuration class for validation parameters"""
    # General validation settings
    validation_enabled: bool = True
    validation_timeout: float = 30.0  # seconds
    max_validation_retries: int = 3

    # Metadata validation settings
    metadata_validation_enabled: bool = True
    required_metadata_fields: list = None
    metadata_validation_timeout: float = 10.0  # seconds

    # Search validation settings
    search_validation_enabled: bool = True
    min_relevance_score: float = 0.5
    max_search_results: int = 10
    search_timeout: float = 15.0  # seconds

    # Performance validation settings
    performance_monitoring_enabled: bool = True
    response_time_threshold: float = 5.0  # seconds
    success_rate_threshold: float = 0.9  # 90%

    # Batch validation settings
    batch_validation_enabled: bool = True
    batch_size: int = 10
    max_concurrent_batches: int = 5

    # Edge case validation settings
    edge_case_validation_enabled: bool = True
    long_query_threshold: int = 500  # characters
    empty_query_threshold: int = 3  # minimum length

    # Reliability validation settings
    reliability_validation_enabled: bool = True
    reliability_iterations: int = 10
    reliability_success_threshold: float = 0.95  # 95%

    # Error handling settings
    error_handling_enabled: bool = True
    max_error_log_size: int = 1000
    error_retry_enabled: bool = True
    error_retry_delay: float = 1.0  # seconds

    # Logging settings
    logging_enabled: bool = True
    log_level: str = "INFO"
    log_validation_details: bool = True

    # Report settings
    report_generation_enabled: bool = True
    auto_generate_reports: bool = True
    report_retention_days: int = 30

    def __post_init__(self):
        """Initialize default values after creation"""
        if self.required_metadata_fields is None:
            self.required_metadata_fields = ['url', 'chunk_id', 'content', 'source', 'created_at']

    @classmethod
    def from_env(cls) -> 'ValidationSettings':
        """Create settings from environment variables"""
        return cls(
            # General validation settings
            validation_enabled=cls._get_bool_env('VALIDATION_ENABLED', True),
            validation_timeout=cls._get_float_env('VALIDATION_TIMEOUT', 30.0),
            max_validation_retries=cls._get_int_env('MAX_VALIDATION_RETRIES', 3),

            # Metadata validation settings
            metadata_validation_enabled=cls._get_bool_env('METADATA_VALIDATION_ENABLED', True),
            required_metadata_fields=cls._get_list_env('REQUIRED_METADATA_FIELDS',
                                                     ['url', 'chunk_id', 'content', 'source', 'created_at']),
            metadata_validation_timeout=cls._get_float_env('METADATA_VALIDATION_TIMEOUT', 10.0),

            # Search validation settings
            search_validation_enabled=cls._get_bool_env('SEARCH_VALIDATION_ENABLED', True),
            min_relevance_score=cls._get_float_env('MIN_RELEVANCE_SCORE', 0.5),
            max_search_results=cls._get_int_env('MAX_SEARCH_RESULTS', 10),
            search_timeout=cls._get_float_env('SEARCH_TIMEOUT', 15.0),

            # Performance validation settings
            performance_monitoring_enabled=cls._get_bool_env('PERFORMANCE_MONITORING_ENABLED', True),
            response_time_threshold=cls._get_float_env('RESPONSE_TIME_THRESHOLD', 5.0),
            success_rate_threshold=cls._get_float_env('SUCCESS_RATE_THRESHOLD', 0.9),

            # Batch validation settings
            batch_validation_enabled=cls._get_bool_env('BATCH_VALIDATION_ENABLED', True),
            batch_size=cls._get_int_env('BATCH_SIZE', 10),
            max_concurrent_batches=cls._get_int_env('MAX_CONCURRENT_BATCHES', 5),

            # Edge case validation settings
            edge_case_validation_enabled=cls._get_bool_env('EDGE_CASE_VALIDATION_ENABLED', True),
            long_query_threshold=cls._get_int_env('LONG_QUERY_THRESHOLD', 500),
            empty_query_threshold=cls._get_int_env('EMPTY_QUERY_THRESHOLD', 3),

            # Reliability validation settings
            reliability_validation_enabled=cls._get_bool_env('RELIABILITY_VALIDATION_ENABLED', True),
            reliability_iterations=cls._get_int_env('RELIABILITY_ITERATIONS', 10),
            reliability_success_threshold=cls._get_float_env('RELIABILITY_SUCCESS_THRESHOLD', 0.95),

            # Error handling settings
            error_handling_enabled=cls._get_bool_env('ERROR_HANDLING_ENABLED', True),
            max_error_log_size=cls._get_int_env('MAX_ERROR_LOG_SIZE', 1000),
            error_retry_enabled=cls._get_bool_env('ERROR_RETRY_ENABLED', True),
            error_retry_delay=cls._get_float_env('ERROR_RETRY_DELAY', 1.0),

            # Logging settings
            logging_enabled=cls._get_bool_env('LOGGING_ENABLED', True),
            log_level=cls._get_str_env('LOG_LEVEL', 'INFO'),
            log_validation_details=cls._get_bool_env('LOG_VALIDATION_DETAILS', True),

            # Report settings
            report_generation_enabled=cls._get_bool_env('REPORT_GENERATION_ENABLED', True),
            auto_generate_reports=cls._get_bool_env('AUTO_GENERATE_REPORTS', True),
            report_retention_days=cls._get_int_env('REPORT_RETENTION_DAYS', 30)
        )

    @staticmethod
    def _get_bool_env(key: str, default: bool) -> bool:
        """Get boolean value from environment variable"""
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')

    @staticmethod
    def _get_int_env(key: str, default: int) -> int:
        """Get integer value from environment variable"""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default

    @staticmethod
    def _get_float_env(key: str, default: float) -> float:
        """Get float value from environment variable"""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return float(value)
        except ValueError:
            return default

    @staticmethod
    def _get_str_env(key: str, default: str) -> str:
        """Get string value from environment variable"""
        value = os.getenv(key)
        return value if value is not None else default

    @staticmethod
    def _get_list_env(key: str, default: list) -> list:
        """Get list value from environment variable (comma-separated)"""
        value = os.getenv(key)
        if value is None:
            return default
        try:
            # Split by comma and strip whitespace
            return [item.strip() for item in value.split(',') if item.strip()]
        except Exception:
            return default


# Global instance of validation settings
validation_settings = ValidationSettings.from_env()


def get_validation_settings() -> ValidationSettings:
    """Get the global validation settings instance"""
    return validation_settings


# Default configuration values for documentation purposes
DEFAULT_CONFIG_VALUES = {
    # General validation settings
    'VALIDATION_ENABLED': 'True',
    'VALIDATION_TIMEOUT': '30.0',
    'MAX_VALIDATION_RETRIES': '3',

    # Metadata validation settings
    'METADATA_VALIDATION_ENABLED': 'True',
    'REQUIRED_METADATA_FIELDS': 'url,chunk_id,content,source,created_at',
    'METADATA_VALIDATION_TIMEOUT': '10.0',

    # Search validation settings
    'SEARCH_VALIDATION_ENABLED': 'True',
    'MIN_RELEVANCE_SCORE': '0.5',
    'MAX_SEARCH_RESULTS': '10',
    'SEARCH_TIMEOUT': '15.0',

    # Performance validation settings
    'PERFORMANCE_MONITORING_ENABLED': 'True',
    'RESPONSE_TIME_THRESHOLD': '5.0',
    'SUCCESS_RATE_THRESHOLD': '0.9',

    # Batch validation settings
    'BATCH_VALIDATION_ENABLED': 'True',
    'BATCH_SIZE': '10',
    'MAX_CONCURRENT_BATCHES': '5',

    # Edge case validation settings
    'EDGE_CASE_VALIDATION_ENABLED': 'True',
    'LONG_QUERY_THRESHOLD': '500',
    'EMPTY_QUERY_THRESHOLD': '3',

    # Reliability validation settings
    'RELIABILITY_VALIDATION_ENABLED': 'True',
    'RELIABILITY_ITERATIONS': '10',
    'RELIABILITY_SUCCESS_THRESHOLD': '0.95',

    # Error handling settings
    'ERROR_HANDLING_ENABLED': 'True',
    'MAX_ERROR_LOG_SIZE': '1000',
    'ERROR_RETRY_ENABLED': 'True',
    'ERROR_RETRY_DELAY': '1.0',

    # Logging settings
    'LOGGING_ENABLED': 'True',
    'LOG_LEVEL': 'INFO',
    'LOG_VALIDATION_DETAILS': 'True',

    # Report settings
    'REPORT_GENERATION_ENABLED': 'True',
    'AUTO_GENERATE_REPORTS': 'True',
    'REPORT_RETENTION_DAYS': '30'
}


def get_default_config_values() -> Dict[str, str]:
    """Get the default configuration values for documentation"""
    return DEFAULT_CONFIG_VALUES