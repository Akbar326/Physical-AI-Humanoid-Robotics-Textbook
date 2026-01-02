"""
Query type detection service for the RAG Agent API
"""

import logging
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass


logger = logging.getLogger(__name__)


class QueryType(Enum):
    """
    Enum for different types of queries
    """
    FACTUAL = "factual"
    ANALYTICAL = "analytical"
    COMPARATIVE = "comparative"
    DEFINITIONAL = "definitional"
    PROCEDURAL = "procedural"
    EVALUATIVE = "evaluative"
    UNKNOWN = "unknown"


@dataclass
class QueryAnalysisResult:
    """
    Result of query analysis
    """
    query_type: QueryType
    confidence: float
    keywords: List[str]
    detected_patterns: List[str]


class QueryAnalyzerService:
    """
    Service for detecting query types and analyzing query characteristics
    """

    def __init__(self):
        # Keywords that indicate different query types
        self.factual_keywords = [
            "what", "when", "where", "who", "how many", "number", "count",
            "define", "describe", "tell me about", "explain", "list"
        ]

        self.analytical_keywords = [
            "why", "how", "analyze", "analyze the", "examine", "evaluate",
            "discuss", "explore", "understand", "what factors", "what causes"
        ]

        self.comparative_keywords = [
            "compare", "contrast", "difference", "similarities", "versus",
            "vs", "between", "rather than", "instead of", "more than", "less than"
        ]

        self.definitional_keywords = [
            "what is", "define", "meaning of", "definition", "explain what",
            "what does", "what means", "define the term"
        ]

        self.procedural_keywords = [
            "how to", "steps to", "process", "procedure", "method",
            "technique", "way to", "guide", "instructions"
        ]

        self.evaluative_keywords = [
            "best", "worst", "should", "recommend", "advantage", "disadvantage",
            "pros and cons", "better", "worse", "effective", "important"
        ]

    def analyze_query(self, query: str) -> QueryAnalysisResult:
        """
        Analyze a query to determine its type and characteristics
        """
        query_lower = query.lower().strip()
        detected_patterns = []
        keyword_matches = []

        # Check for definitional patterns
        if any(keyword in query_lower for keyword in self.definitional_keywords):
            detected_patterns.append("definitional")
            keyword_matches.extend([
                kw for kw in self.definitional_keywords if kw in query_lower
            ])

        # Check for factual patterns
        if any(keyword in query_lower for keyword in self.factual_keywords):
            detected_patterns.append("factual")
            keyword_matches.extend([
                kw for kw in self.factual_keywords if kw in query_lower
            ])

        # Check for analytical patterns
        if any(keyword in query_lower for keyword in self.analytical_keywords):
            detected_patterns.append("analytical")
            keyword_matches.extend([
                kw for kw in self.analytical_keywords if kw in query_lower
            ])

        # Check for comparative patterns
        if any(keyword in query_lower for keyword in self.comparative_keywords):
            detected_patterns.append("comparative")
            keyword_matches.extend([
                kw for kw in self.comparative_keywords if kw in query_lower
            ])

        # Check for procedural patterns
        if any(keyword in query_lower for keyword in self.procedural_keywords):
            detected_patterns.append("procedural")
            keyword_matches.extend([
                kw for kw in self.procedural_keywords if kw in query_lower
            ])

        # Check for evaluative patterns
        if any(keyword in query_lower for keyword in self.evaluative_keywords):
            detected_patterns.append("evaluative")
            keyword_matches.extend([
                kw for kw in self.evaluative_keywords if kw in query_lower
            ])

        # Determine the most likely query type based on detected patterns
        query_type = self._determine_query_type(detected_patterns)

        # Calculate confidence based on number of matching keywords
        confidence = min(len(set(keyword_matches)) * 0.15, 1.0)  # Max 100% confidence

        result = QueryAnalysisResult(
            query_type=query_type,
            confidence=confidence,
            keywords=list(set(keyword_matches)),
            detected_patterns=detected_patterns
        )

        logger.info(f"Query analysis result: {query_type.value} (confidence: {confidence:.2f}) for query: {query[:50]}...")
        return result

    def _determine_query_type(self, detected_patterns: List[str]) -> QueryType:
        """
        Determine the primary query type from detected patterns
        """
        if not detected_patterns:
            return QueryType.UNKNOWN

        # Priority order for determining query type
        priority_order = [
            ("definitional", QueryType.DEFINITIONAL),
            ("comparative", QueryType.COMPARATIVE),
            ("analytical", QueryType.ANALYTICAL),
            ("procedural", QueryType.PROCEDURAL),
            ("evaluative", QueryType.EVALUATIVE),
            ("factual", QueryType.FACTUAL)
        ]

        for pattern, query_type in priority_order:
            if pattern in detected_patterns:
                return query_type

        return QueryType.UNKNOWN

    def is_factual_query(self, query: str) -> bool:
        """
        Check if a query is primarily factual
        """
        result = self.analyze_query(query)
        return result.query_type == QueryType.FACTUAL

    def is_analytical_query(self, query: str) -> bool:
        """
        Check if a query is primarily analytical
        """
        result = self.analyze_query(query)
        return result.query_type == QueryType.ANALYTICAL

    def is_comparative_query(self, query: str) -> bool:
        """
        Check if a query is primarily comparative
        """
        result = self.analyze_query(query)
        return result.query_type == QueryType.COMPARATIVE


# Global instance for convenience
query_analyzer_service = QueryAnalyzerService()