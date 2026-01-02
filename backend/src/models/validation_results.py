"""
Validation result data structures
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime


@dataclass
class SearchValidationResult:
    """Result of a search validation operation"""
    query: str
    results: List[Dict[str, Any]]
    relevance_score: float
    metadata_accuracy: bool
    response_time: float
    passed: bool
    validation_details: Optional[Dict[str, Any]] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

        # Validate relevance score range
        if not 0.0 <= self.relevance_score <= 1.0:
            raise ValueError("Relevance score must be between 0.0 and 1.0")

        # Validate response time is non-negative
        if self.response_time < 0:
            raise ValueError("Response time must be non-negative")


@dataclass
class BatchValidationResult:
    """Result of a batch validation operation"""
    scenario_name: str
    total_tests: int
    passed_tests: int
    success_rate: float
    average_response_time: float
    detailed_results: List[SearchValidationResult]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

        # Validate success rate range
        if not 0.0 <= self.success_rate <= 1.0:
            raise ValueError("Success rate must be between 0.0 and 1.0")

        # Validate average response time is non-negative
        if self.average_response_time < 0:
            raise ValueError("Average response time must be non-negative")


@dataclass
class MetadataValidationResult:
    """Result of a metadata validation operation"""
    query: str
    metadata_validation: Dict[str, bool]
    validation_passed: bool
    issues: List[str]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class PipelineReliabilityResult:
    """Result of pipeline reliability validation"""
    success_rate: float
    total_queries: int
    successful_queries: int
    failed_queries: int
    average_response_time: float
    p95_response_time: float
    issues: List[str]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

        # Validate success rate range
        if not 0.0 <= self.success_rate <= 1.0:
            raise ValueError("Success rate must be between 0.0 and 1.0")

        # Validate response times are non-negative
        if self.average_response_time < 0 or self.p95_response_time < 0:
            raise ValueError("Response times must be non-negative")


@dataclass
class ValidationSummary:
    """Summary of validation results"""
    total_validations: int
    successful_validations: int
    failed_validations: int
    success_rate: float
    average_response_time: float
    validation_results: List[SearchValidationResult]
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

        # Validate success rate range
        if not 0.0 <= self.success_rate <= 1.0:
            raise ValueError("Success rate must be between 0.0 and 1.0")

        # Validate average response time is non-negative
        if self.average_response_time < 0:
            raise ValueError("Average response time must be non-negative")