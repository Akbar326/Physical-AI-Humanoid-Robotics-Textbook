"""
Unit tests for semantic search validation
"""

import unittest
from unittest.mock import Mock, patch
from src.services.semantic_search_validator import SemanticSearchValidator
from src.models.validation import TestQuery, RetrievedChunk


class TestSemanticSearchValidator(unittest.TestCase):
    """Unit tests for SemanticSearchValidator"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = SemanticSearchValidator()

    def test_validate_success_with_relevant_results(self):
        """Test validation succeeds when results are relevant to query"""
        test_query = TestQuery(
            query_text="AI robotics",
            expected_concepts=["artificial intelligence", "robotics"],
            category="ai_robotics"
        )

        # Mock search service to return relevant results
        with patch.object(self.validator.search_service, 'search') as mock_search:
            mock_search.return_value = [
                RetrievedChunk(
                    chunk_id="test_chunk_1",
                    content="Artificial intelligence in robotics enables machines to perceive, reason, and act in complex environments",
                    source_url="https://example.com/ai-robotics",
                    relevance_score=0.9,
                    position=1,
                    metadata={"test": "data"}
                )
            ]

            result = self.validator.validate(test_query)

            self.assertTrue(result.success)
            self.assertIsNotNone(result.details)
            self.assertIn('relevance_score', result.details)

    def test_validate_failure_with_no_results(self):
        """Test validation fails when no results are returned"""
        test_query = TestQuery(
            query_text="nonexistent concept",
            expected_concepts=["some concept"],
            category="test"
        )

        # Mock search service to return no results
        with patch.object(self.validator.search_service, 'search') as mock_search:
            mock_search.return_value = []

            result = self.validator.validate(test_query)

            self.assertFalse(result.success)
            self.assertIn("No results found", result.message)

    def test_validate_with_partial_concept_match(self):
        """Test validation with partial concept matching"""
        test_query = TestQuery(
            query_text="machine learning algorithms",
            expected_concepts=["machine learning", "neural networks", "decision trees"],
            category="ml"
        )

        # Mock search service to return results with partial concept match
        with patch.object(self.validator.search_service, 'search') as mock_search:
            mock_search.return_value = [
                RetrievedChunk(
                    chunk_id="test_chunk_1",
                    content="Machine learning algorithms are a subset of artificial intelligence that enable systems to learn and improve from experience",
                    source_url="https://example.com/ml",
                    relevance_score=0.8,
                    position=1,
                    metadata={"test": "data"}
                )
            ]

            result = self.validator.validate(test_query)

            # Should succeed since at least one concept is found
            self.assertTrue(result.success)

    def test_calculate_relevance_score_perfect_match(self):
        """Test relevance score calculation with perfect concept match"""
        results = [
            RetrievedChunk(
                chunk_id="test_chunk_1",
                content="Artificial intelligence and robotics are closely related fields",
                source_url="https://example.com/test",
                relevance_score=0.9,
                position=1,
                metadata={}
            )
        ]
        expected_concepts = ["artificial intelligence", "robotics"]

        score = self.validator._calculate_relevance_score(results, expected_concepts)

        # Score should be reasonably high with perfect concept match
        self.assertGreater(score, 0.5)

    def test_calculate_relevance_score_no_match(self):
        """Test relevance score calculation with no concept match"""
        results = [
            RetrievedChunk(
                chunk_id="test_chunk_1",
                content="This content is unrelated to AI or robotics",
                source_url="https://example.com/test",
                relevance_score=0.1,
                position=1,
                metadata={}
            )
        ]
        expected_concepts = ["artificial intelligence", "robotics"]

        score = self.validator._calculate_relevance_score(results, expected_concepts)

        # Score should be low with no concept match
        self.assertLess(score, 0.5)

    def test_check_concepts_in_results(self):
        """Test concept checking in results"""
        results = [
            RetrievedChunk(
                chunk_id="test_chunk_1",
                content="Artificial intelligence and robotics are related fields",
                source_url="https://example.com/test",
                relevance_score=0.8,
                position=1,
                metadata={}
            )
        ]
        expected_concepts = ["artificial intelligence", "robotics", "unrelated concept"]

        concepts_found = self.validator._check_concepts_in_results(results, expected_concepts)

        self.assertEqual(concepts_found["artificial intelligence"], True)
        self.assertEqual(concepts_found["robotics"], True)
        self.assertEqual(concepts_found["unrelated concept"], False)

    def test_validate_batch(self):
        """Test batch validation"""
        test_queries = [
            TestQuery(
                query_text="AI",
                expected_concepts=["artificial intelligence"],
                category="ai"
            ),
            TestQuery(
                query_text="robotics",
                expected_concepts=["robots"],
                category="robotics"
            )
        ]

        # Mock search service for all queries
        with patch.object(self.validator.search_service, 'search') as mock_search:
            mock_search.return_value = [
                RetrievedChunk(
                    chunk_id="test_chunk",
                    content="Artificial intelligence is a field",
                    source_url="https://example.com/test",
                    relevance_score=0.8,
                    position=1,
                    metadata={}
                )
            ]

            results = self.validator.validate_batch(test_queries)

            self.assertEqual(len(results), 2)
            for result in results:
                self.assertIsInstance(result.success, bool)


if __name__ == '__main__':
    unittest.main()