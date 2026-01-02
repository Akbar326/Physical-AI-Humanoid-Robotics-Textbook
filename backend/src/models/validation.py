"""
Validation models based on the data model specification
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime


@dataclass
class TestQuery:
    """Model representing a test query for validation"""
    query_text: str
    expected_concepts: List[str]
    category: str
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

        # Validate query_text length
        if len(self.query_text) < 1 or len(self.query_text) > 500:
            raise ValueError("Query text must be between 1 and 500 characters")


@dataclass
class RetrievedChunk:
    """Model representing a retrieved text chunk from search"""
    chunk_id: str
    content: str
    source_url: str
    relevance_score: float
    position: int
    metadata: Dict[str, Any]

    def __post_init__(self):
        # Validate relevance score range
        if not 0.0 <= self.relevance_score <= 1.0:
            raise ValueError("Relevance score must be between 0.0 and 1.0")


@dataclass
class ValidationCriterion:
    """Model representing a validation criterion"""
    name: str
    description: str
    threshold: float
    metric: str


@dataclass
class TestScenario:
    """Model representing a test scenario"""
    name: str
    description: str
    queries: List[TestQuery]
    success_criteria: List[ValidationCriterion]
    category: str


@dataclass
class ValidationResult:
    """Model representing the result of a validation"""
    query_id: str
    retrieved_chunks: List[RetrievedChunk]
    relevance_score: float
    metadata_accuracy: bool
    response_time: float
    passed: bool
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