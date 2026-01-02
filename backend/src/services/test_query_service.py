"""
Test query execution service
"""

from typing import List, Dict, Any
import logging
import time
from src.models.validation import TestQuery
from src.services.search_service import SearchService
from src.services.semantic_search_validator import SemanticSearchValidator

logger = logging.getLogger(__name__)


class TestQueryService:
    """Service for executing test queries and managing test execution"""

    def __init__(self):
        self.search_service = SearchService()
        self.validator = SemanticSearchValidator()

    def execute_single_test_query(self, test_query: TestQuery) -> Dict[str, Any]:
        """Execute a single test query and return results with validation"""
        start_time = time.time()

        # Perform the search
        search_results = self.search_service.search(test_query.query_text, top_k=5)

        # Validate the results
        validation_result = self.validator.validate(test_query)

        execution_time = time.time() - start_time

        return {
            'query': test_query.query_text,
            'results': search_results,
            'validation_result': validation_result,
            'execution_time': execution_time,
            'expected_concepts': test_query.expected_concepts,
            'category': test_query.category
        }

    def execute_batch_test_queries(self, test_queries: List[TestQuery]) -> List[Dict[str, Any]]:
        """Execute multiple test queries in batch"""
        results = []
        for query in test_queries:
            result = self.execute_single_test_query(query)
            results.append(result)
        return results

    def execute_test_scenario(self, queries: List[TestQuery], scenario_name: str = "Default Scenario") -> Dict[str, Any]:
        """Execute a complete test scenario with multiple queries"""
        start_time = time.time()

        # Execute all queries in the scenario
        scenario_results = self.execute_batch_test_queries(queries)

        # Calculate scenario metrics
        total_queries = len(scenario_results)
        successful_queries = sum(1 for r in scenario_results if r['validation_result'].success)
        success_rate = successful_queries / total_queries if total_queries > 0 else 0

        total_execution_time = time.time() - start_time

        # Calculate average response time
        avg_response_time = sum(r['execution_time'] for r in scenario_results) / total_queries if total_queries > 0 else 0

        return {
            'scenario_name': scenario_name,
            'total_queries': total_queries,
            'successful_queries': successful_queries,
            'success_rate': success_rate,
            'total_execution_time': total_execution_time,
            'average_response_time': avg_response_time,
            'results': scenario_results
        }

    def create_test_query(self, query_text: str, expected_concepts: List[str], category: str) -> TestQuery:
        """Create a TestQuery instance with validation"""
        return TestQuery(
            query_text=query_text,
            expected_concepts=expected_concepts,
            category=category
        )

    def run_predefined_test_suite(self) -> Dict[str, Any]:
        """Run a predefined suite of test queries for basic semantic search"""
        # Define test queries for basic semantic search
        test_queries = [
            self.create_test_query(
                query_text="AI robotics fundamentals",
                expected_concepts=["artificial intelligence", "robotics", "machine learning"],
                category="ai_robotics"
            ),
            self.create_test_query(
                query_text="humanoid movement principles",
                expected_concepts=["locomotion", "bipedal", "motion planning", "kinematics"],
                category="humanoid_movement"
            ),
            self.create_test_query(
                query_text="physical AI concepts",
                expected_concepts=["embodied AI", "physical interaction", "robotics"],
                category="physical_ai"
            )
        ]

        return self.execute_test_scenario(test_queries, "Basic Semantic Search Test Suite")

    def validate_query_relevance(self, query_text: str, expected_concepts: List[str], top_k: int = 5) -> Dict[str, Any]:
        """Validate relevance of search results for a specific query"""
        # Create a temporary test query
        test_query = self.create_test_query(query_text, expected_concepts, "relevance_test")

        # Execute the query
        result = self.execute_single_test_query(test_query)

        # Calculate relevance metrics
        found_concepts = []
        if result['results']:
            content_text = " ".join([r.content.lower() for r in result['results']])
            found_concepts = [concept for concept in expected_concepts if concept.lower() in content_text]

        relevance_percentage = len(found_concepts) / len(expected_concepts) if expected_concepts else 0

        result['relevance_metrics'] = {
            'expected_concepts': expected_concepts,
            'found_concepts': found_concepts,
            'relevance_percentage': relevance_percentage,
            'total_results': len(result['results'])
        }

        return result

    def get_performance_metrics(self, test_queries: List[TestQuery]) -> Dict[str, Any]:
        """Get performance metrics for a set of test queries"""
        start_time = time.time()

        execution_times = []
        success_count = 0

        for query in test_queries:
            query_start = time.time()
            result = self.execute_single_test_query(query)
            query_time = time.time() - query_start
            execution_times.append(query_time)

            if result['validation_result'].success:
                success_count += 1

        total_time = time.time() - start_time

        return {
            'total_time': total_time,
            'average_query_time': sum(execution_times) / len(execution_times) if execution_times else 0,
            'min_query_time': min(execution_times) if execution_times else 0,
            'max_query_time': max(execution_times) if execution_times else 0,
            'success_rate': success_count / len(test_queries) if test_queries else 0,
            'total_queries': len(test_queries),
            'successful_queries': success_count
        }