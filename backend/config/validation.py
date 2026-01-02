"""
Configuration for validation components
"""

import os
from typing import Optional

# Validation-specific settings
DEFAULT_TOP_K_RESULTS = 5
MAX_QUERY_LENGTH = 500
MIN_RELEVANCE_SCORE = 0.7
MAX_RESPONSE_TIME_SECONDS = 2.0
SUCCESS_RATE_THRESHOLD = 0.95

# Test scenario settings
BATCH_TEST_TIMEOUT = 30  # seconds
EDGE_CASE_TEST_QUERIES = [
    "AI robotics",
    "humanoid movement",
    "physical AI",
    "machine learning",
    "kinematics",
    "motion planning"
]

def get_validation_config():
    """Return validation configuration based on environment"""
    return {
        'default_top_k': int(os.getenv('VALIDATION_DEFAULT_TOP_K', DEFAULT_TOP_K_RESULTS)),
        'max_query_length': int(os.getenv('VALIDATION_MAX_QUERY_LENGTH', MAX_QUERY_LENGTH)),
        'min_relevance_score': float(os.getenv('VALIDATION_MIN_RELEVANCE_SCORE', MIN_RELEVANCE_SCORE)),
        'max_response_time': float(os.getenv('VALIDATION_MAX_RESPONSE_TIME', MAX_RESPONSE_TIME_SECONDS)),
        'success_rate_threshold': float(os.getenv('VALIDATION_SUCCESS_RATE_THRESHOLD', SUCCESS_RATE_THRESHOLD)),
        'batch_test_timeout': int(os.getenv('VALIDATION_BATCH_TEST_TIMEOUT', BATCH_TEST_TIMEOUT)),
        'edge_case_queries': os.getenv('VALIDATION_EDGE_CASE_QUERIES', EDGE_CASE_TEST_QUERIES)
    }