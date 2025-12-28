"""
Integration tests for basic search functionality validation
"""

import unittest
import os
from src.services.search_service import SearchService
from src.services.test_query_service import TestQueryService
from src.validation.test_executor import TestExecutor
from src.models.validation import TestQuery


class TestBasicSearchIntegration(unittest.TestCase):
    """Integration tests for basic search functionality"""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before running tests in the class"""
        # Check if we have the required environment variables
        cls.has_cohere_key = bool(os.getenv('COHERE_API_KEY'))
        cls.has_qdrant_config = all([
            os.getenv('QDRANT_API_KEY'),
            os.getenv('QDRANT_HOST')
        ])

    def setUp(self):
        """Set up test fixtures"""
        if not (self.has_cohere_key and self.has_qdrant_config):
            # Skip tests if we don't have proper configuration
            self.skipTest("Missing required environment configuration for integration tests")

        self.search_service = SearchService()
        self.test_query_service = TestQueryService()
        self.test_executor = TestExecutor()

    def test_search_service_initialization(self):
        """Test that search service initializes correctly"""
        self.assertIsNotNone(self.search_service.qdrant_helper)
        self.assertIsNotNone(self.search_service.cohere_client)

    @unittest.skipIf(not (TestBasicSearchIntegration.has_cohere_key and TestBasicSearchIntegration.has_qdrant_config),
                     "Missing required environment configuration for integration tests")
    def test_embed_query_functionality(self):
        """Test that query embedding works"""
        query_text = "AI robotics"
        embedding = self.search_service.embed_query(query_text)

        # Check that embedding is returned
        self.assertIsNotNone(embedding)
        self.assertIsInstance(embedding, list)
        # Cohere embeddings for embed-english-v3.0 should be 1024-dimensional
        self.assertEqual(len(embedding), 1024)

    @unittest.skipIf(not (TestBasicSearchIntegration.has_cohere_key and TestBasicSearchIntegration.has_qdrant_config),
                     "Missing required environment configuration for integration tests")
    def test_search_functionality(self):
        """Test that search functionality works end-to-end"""
        query_text = "AI robotics"
        results = self.search_service.search(query_text, top_k=3)

        # Check that results are returned
        self.assertIsInstance(results, list)
        # Results might be empty if the collection doesn't have matching content
        # but the call should succeed
        for result in results:
            self.assertIsNotNone(result.chunk_id)
            self.assertIsNotNone(result.content)
            self.assertIsNotNone(result.source_url)
            self.assertIsInstance(result.relevance_score, float)

    @unittest.skipIf(not (TestBasicSearchIntegration.has_cohere_key and TestBasicSearchIntegration.has_qdrant_config),
                     "Missing required environment configuration for integration tests")
    def test_test_query_service_execution(self):
        """Test that test query service can execute a test query"""
        test_query = TestQuery(
            query_text="AI robotics",
            expected_concepts=["artificial intelligence", "robotics"],
            category="ai_robotics"
        )

        result = self.test_query_service.execute_single_test_query(test_query)

        # Check that result structure is correct
        self.assertIn('query', result)
        self.assertIn('results', result)
        self.assertIn('validation_result', result)
        self.assertIn('execution_time', result)

    @unittest.skipIf(not (TestBasicSearchIntegration.has_cohere_key and TestBasicSearchIntegration.has_qdrant_config),
                     "Missing required environment configuration for integration tests")
    def test_test_execution_framework(self):
        """Test the test execution framework"""
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

        result = self.test_executor.execute_test_suite(test_queries, "Integration Test Suite")

        # Check that results are returned with proper structure
        self.assertIn('suite_name', result)
        self.assertIn('total_tests', result)
        self.assertIn('successful_tests', result)
        self.assertIn('results', result)
        self.assertEqual(result['total_tests'], 2)

    @unittest.skipIf(not (TestBasicSearchIntegration.has_cohere_key and TestBasicSearchIntegration.has_qdrant_config),
                     "Missing required environment configuration for integration tests")
    def test_validate_search_functionality(self):
        """Test search validation functionality"""
        success = self.search_service.validate_search_functionality("AI robotics")
        # This should return a boolean indicating if search is functional
        self.assertIsInstance(success, bool)

    @unittest.skipIf(not (TestBasicSearchIntegration.has_cohere_key and TestBasicSearchIntegration.has_qdrant_config),
                     "Missing required environment configuration for integration tests")
    def test_performance_metrics(self):
        """Test performance metrics collection"""
        query_text = "AI"
        metrics = self.search_service.get_search_performance_metrics(query_text, iterations=2)

        # Check that metrics are returned with proper structure
        self.assertIn('average_response_time', metrics)
        self.assertIn('success_rate', metrics)
        self.assertIn('total_time', metrics)
        self.assertIn('iterations', metrics)

        # Verify types
        self.assertIsInstance(metrics['average_response_time'], float)
        self.assertIsInstance(metrics['success_rate'], float)
        self.assertIsInstance(metrics['total_time'], float)
        self.assertIsInstance(metrics['iterations'], int)


class TestBasicSearchIntegrationWithoutExternalServices(unittest.TestCase):
    """
    Integration tests that don't require external services
    These test the integration between our internal components
    """

    def setUp(self):
        """Set up test fixtures without external dependencies"""
        # Create services with mocked external dependencies
        self.test_query_service = TestQueryService()
        self.test_executor = TestExecutor()

    def test_internal_component_integration(self):
        """Test integration between internal components without external services"""
        # Create a test query
        test_query = TestQuery(
            query_text="test query for integration",
            expected_concepts=["test", "integration"],
            category="integration"
        )

        # Execute the test query (this will use mock embeddings since cohere isn't configured)
        result = self.test_query_service.execute_single_test_query(test_query)

        # Check that the result has the expected structure
        self.assertIn('query', result)
        self.assertIn('results', result)  # May be empty if no collection exists
        self.assertIn('validation_result', result)
        self.assertIn('execution_time', result)

        # Check that validation result has proper structure
        validation_result = result['validation_result']
        self.assertIsNotNone(validation_result)

    def test_test_executor_with_mock_data(self):
        """Test test executor with mock data"""
        # Create test queries
        test_queries = [
            TestQuery(
                query_text="first test query",
                expected_concepts=["test"],
                category="integration"
            ),
            TestQuery(
                query_text="second test query",
                expected_concepts=["query"],
                category="integration"
            )
        ]

        # Execute the test suite
        result = self.test_executor.execute_test_suite(test_queries, "Mock Integration Test Suite")

        # Verify structure of results
        self.assertEqual(result['suite_name'], "Mock Integration Test Suite")
        self.assertEqual(result['total_tests'], 2)
        self.assertIsInstance(result['results'], list)
        self.assertEqual(len(result['results']), 2)

        # Verify that each result is a ValidationResult
        for validation_result in result['results']:
            self.assertIsNotNone(validation_result)


if __name__ == '__main__':
    unittest.main()