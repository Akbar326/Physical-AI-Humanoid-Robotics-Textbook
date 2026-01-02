"""
Batch test execution service for running multiple validation tests
"""

from typing import List, Dict, Any
import time
import logging
from src.models.validation import TestScenario, ValidationResult
from src.services.search_service import SearchService
from src.services.test_query_service import TestQueryService
from src.services.validation_service import ValidationService, ValidationResult as ServiceValidationResult


logger = logging.getLogger(__name__)


class BatchTestService:
    """Service for executing batch tests across multiple scenarios"""

    def __init__(self):
        self.search_service = SearchService()
        self.test_query_service = TestQueryService()
        self.execution_results = []

    def execute_batch_tests(self, scenarios: List[TestScenario], max_concurrent: int = 5) -> Dict[str, Any]:
        """
        Execute a batch of test scenarios

        Args:
            scenarios: List of test scenarios to execute
            max_concurrent: Maximum number of concurrent tests (not used in basic implementation)

        Returns:
            Dictionary with execution results and statistics
        """
        start_time = time.time()
        results = []

        for scenario in scenarios:
            logger.info(f"Executing scenario: {scenario.name}")

            scenario_results = []
            for query in scenario.queries:
                # Execute the test query
                query_result = self.test_query_service.execute_single_test_query(query)
                scenario_results.append(query_result)

            results.append({
                'scenario_name': scenario.name,
                'scenario_description': scenario.description,
                'query_results': scenario_results,
                'success_criteria': scenario.success_criteria
            })

        total_time = time.time() - start_time

        # Calculate statistics
        total_queries = sum(len(result['query_results']) for result in results)
        successful_queries = 0
        total_response_time = 0

        for result in results:
            for query_result in result['query_results']:
                if query_result.get('validation_result', {}).get('passed', False):
                    successful_queries += 1
                total_response_time += query_result.get('execution_time', 0)

        stats = {
            'total_scenarios': len(scenarios),
            'total_queries': total_queries,
            'successful_queries': successful_queries,
            'failed_queries': total_queries - successful_queries,
            'success_rate': successful_queries / total_queries if total_queries > 0 else 0,
            'total_execution_time': total_time,
            'average_response_time': total_response_time / total_queries if total_queries > 0 else 0,
            'results': results
        }

        return stats

    def execute_stress_test(self, base_query: str, iterations: int = 100, delay: float = 0.1) -> Dict[str, Any]:
        """
        Execute a stress test by running the same query multiple times

        Args:
            base_query: The query to run multiple times
            iterations: Number of times to run the query
            delay: Delay between queries in seconds

        Returns:
            Dictionary with stress test results and statistics
        """
        start_time = time.time()
        results = []

        for i in range(iterations):
            query_result = self.test_query_service.execute_single_test_query_from_text(base_query)
            results.append(query_result)

            if delay > 0:
                time.sleep(delay)

            if i % 10 == 0:  # Log progress every 10 iterations
                logger.info(f"Stress test progress: {i}/{iterations}")

        total_time = time.time() - start_time

        # Calculate stress test statistics
        successful_tests = sum(1 for result in results if result.get('validation_result', {}).get('passed', False))
        response_times = [result.get('execution_time', 0) for result in results]

        stats = {
            'iterations': iterations,
            'successful_tests': successful_tests,
            'failed_tests': iterations - successful_tests,
            'success_rate': successful_tests / iterations if iterations > 0 else 0,
            'total_execution_time': total_time,
            'average_response_time': sum(response_times) / len(response_times) if response_times else 0,
            'min_response_time': min(response_times) if response_times else 0,
            'max_response_time': max(response_times) if response_times else 0,
            'results': results
        }

        return stats

    def execute_reliability_test(self, scenarios: List[TestScenario], iterations_per_scenario: int = 10) -> Dict[str, Any]:
        """
        Execute reliability test by running each scenario multiple times

        Args:
            scenarios: List of scenarios to test for reliability
            iterations_per_scenario: Number of times to run each scenario

        Returns:
            Dictionary with reliability test results and statistics
        """
        start_time = time.time()
        scenario_results = []

        for scenario in scenarios:
            logger.info(f"Running reliability test for scenario: {scenario.name}")

            iteration_results = []
            for i in range(iterations_per_scenario):
                # Execute the scenario once
                scenario_result = self.execute_single_scenario(scenario)
                iteration_results.append(scenario_result)

            # Calculate statistics for this scenario
            successful_iterations = sum(1 for result in iteration_results
                                      if result.get('success_rate', 0) >= 0.9)  # Assuming 90% success is "successful"

            scenario_stats = {
                'scenario_name': scenario.name,
                'scenario_description': scenario.description,
                'iterations': iterations_per_scenario,
                'successful_iterations': successful_iterations,
                'failed_iterations': iterations_per_scenario - successful_iterations,
                'reliability_rate': successful_iterations / iterations_per_scenario if iterations_per_scenario > 0 else 0,
                'iteration_results': iteration_results
            }

            scenario_results.append(scenario_stats)

        total_time = time.time() - start_time

        # Calculate overall reliability statistics
        total_iterations = sum(result['iterations'] for result in scenario_results)
        total_successful = sum(result['successful_iterations'] for result in scenario_results)

        overall_stats = {
            'total_scenarios': len(scenarios),
            'total_iterations': total_iterations,
            'total_successful_iterations': total_successful,
            'total_failed_iterations': total_iterations - total_successful,
            'overall_reliability_rate': total_successful / total_iterations if total_iterations > 0 else 0,
            'total_execution_time': total_time,
            'scenario_results': scenario_results
        }

        return overall_stats

    def execute_single_scenario(self, scenario: TestScenario) -> Dict[str, Any]:
        """
        Execute a single scenario and return results

        Args:
            scenario: The test scenario to execute

        Returns:
            Dictionary with execution results
        """
        query_results = []

        for query in scenario.queries:
            query_result = self.test_query_service.execute_single_test_query(query)
            query_results.append(query_result)

        # Calculate statistics for this execution
        successful_queries = sum(1 for result in query_results
                               if result.get('validation_result', {}).get('passed', False))
        total_queries = len(query_results)

        return {
            'query_results': query_results,
            'total_queries': total_queries,
            'successful_queries': successful_queries,
            'failed_queries': total_queries - successful_queries,
            'success_rate': successful_queries / total_queries if total_queries > 0 else 0,
            'success_criteria': scenario.success_criteria
        }

    def validate_batch_results(self, batch_results: Dict[str, Any], success_criteria: List[Dict[str, Any]] = None) -> ServiceValidationResult:
        """
        Validate the results of a batch test against success criteria

        Args:
            batch_results: Results from a batch test execution
            success_criteria: List of criteria that must be met for success

        Returns:
            Validation result indicating if batch test was successful
        """
        if success_criteria is None:
            # Default success criteria
            success_criteria = [
                {'metric': 'success_rate', 'threshold': 0.9, 'comparison': 'gte'},  # 90% success rate
                {'metric': 'average_response_time', 'threshold': 5.0, 'comparison': 'lte'}  # 5 seconds max average response time
            ]

        validation_results = []

        for criterion in success_criteria:
            metric = criterion['metric']
            threshold = criterion['threshold']
            comparison = criterion['comparison']

            actual_value = batch_results.get(metric, 0)

            if comparison == 'gte':
                is_valid = actual_value >= threshold
            elif comparison == 'lte':
                is_valid = actual_value <= threshold
            elif comparison == 'gt':
                is_valid = actual_value > threshold
            elif comparison == 'lt':
                is_valid = actual_value < threshold
            elif comparison == 'eq':
                is_valid = actual_value == threshold
            else:
                is_valid = False

            validation_results.append({
                'criterion': criterion,
                'actual_value': actual_value,
                'is_valid': is_valid
            })

        # Overall success is True only if all criteria pass
        overall_success = all(result['is_valid'] for result in validation_results)

        return ServiceValidationResult(
            success=overall_success,
            message=f"Batch test {'passed' if overall_success else 'failed'} validation",
            details={
                'validation_results': validation_results,
                'total_criteria': len(validation_results),
                'passed_criteria': sum(1 for r in validation_results if r['is_valid'])
            }
        )