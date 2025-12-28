"""
Semantic search validation service
"""

from typing import List, Dict, Any
import logging
from src.services.validation_service import ValidationService, ValidationResult
from src.services.search_service import SearchService
from src.models.validation import TestQuery, RetrievedChunk

logger = logging.getLogger(__name__)


class SemanticSearchValidator(ValidationService):
    """Validator for semantic search functionality"""

    def __init__(self):
        super().__init__()
        self.search_service = SearchService()

    def validate(self, test_query: TestQuery) -> ValidationResult:
        """
        Validate semantic search for a given test query
        """
        try:
            # Perform search using the test query
            results = self.search_service.search(test_query.query_text, top_k=5)

            if not results:
                return ValidationResult(
                    success=False,
                    message=f"No results found for query: {test_query.query_text}",
                    details={'query': test_query.query_text, 'results_count': 0}
                )

            # Check if results contain expected concepts
            relevance_score = self._calculate_relevance_score(results, test_query.expected_concepts)

            # Validate that expected concepts are present in results
            concepts_found = self._check_concepts_in_results(results, test_query.expected_concepts)

            success = relevance_score >= 0.3  # Using 0.3 as minimum relevance threshold
            message = f"Search validation {'passed' if success else 'failed'} with relevance score {relevance_score:.2f}"

            details = {
                'query': test_query.query_text,
                'results_count': len(results),
                'relevance_score': relevance_score,
                'concepts_found': concepts_found,
                'expected_concepts': test_query.expected_concepts,
                'retrieved_content_preview': [r.content[:100] + "..." for r in results[:3]]  # Preview of top 3 results
            }

            return ValidationResult(
                success=success,
                message=message,
                details=details
            )
        except Exception as e:
            logger.error(f"Error validating semantic search: {str(e)}", exc_info=True)
            return ValidationResult(
                success=False,
                message=f"Error during semantic search validation: {str(e)}",
                details={'query': test_query.query_text if test_query else 'unknown'}
            )

    def _calculate_relevance_score(self, results: List[RetrievedChunk], expected_concepts: List[str]) -> float:
        """
        Calculate relevance score based on how well results match expected concepts
        """
        if not results or not expected_concepts:
            return 0.0

        # Calculate how many expected concepts are found in the results
        content_text = " ".join([r.content.lower() for r in results])

        found_concepts = []
        for concept in expected_concepts:
            if concept.lower() in content_text:
                found_concepts.append(concept)

        # Calculate score as ratio of found concepts to expected concepts
        relevance_score = len(found_concepts) / len(expected_concepts) if expected_concepts else 0.0

        # Boost score based on relevance scores of individual results
        avg_relevance = sum(r.relevance_score for r in results) / len(results)
        relevance_score = (relevance_score + avg_relevance) / 2

        return min(relevance_score, 1.0)  # Cap at 1.0

    def _check_concepts_in_results(self, results: List[RetrievedChunk], expected_concepts: List[str]) -> Dict[str, bool]:
        """
        Check which expected concepts are found in the results
        """
        content_text = " ".join([r.content.lower() for r in results])

        concepts_found = {}
        for concept in expected_concepts:
            concepts_found[concept] = concept.lower() in content_text

        return concepts_found

    def validate_batch(self, test_queries: List[TestQuery]) -> List[ValidationResult]:
        """
        Validate multiple test queries in batch
        """
        results = []
        for query in test_queries:
            result = self.validate(query)
            results.append(result)
        return results

    def validate_with_detailed_metrics(self, test_query: TestQuery) -> Dict[str, Any]:
        """
        Perform validation and return detailed metrics
        """
        validation_result = self.validate(test_query)

        results = self.search_service.search(test_query.query_text, top_k=5)

        detailed_metrics = {
            'validation_result': validation_result,
            'query_details': {
                'query_text': test_query.query_text,
                'category': test_query.category,
                'expected_concepts': test_query.expected_concepts
            },
            'search_results': [
                {
                    'chunk_id': r.chunk_id,
                    'content_preview': r.content[:200] + "...",
                    'relevance_score': r.relevance_score,
                    'source_url': r.source_url,
                    'position': r.position
                } for r in results
            ],
            'metrics': {
                'total_results': len(results),
                'avg_relevance_score': sum(r.relevance_score for r in results) / len(results) if results else 0,
                'top_result_score': results[0].relevance_score if results else 0
            }
        }

        return detailed_metrics