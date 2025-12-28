"""
Test execution framework
"""

from typing import List, Dict, Any
import logging
import time
from datetime import datetime
from src.models.validation import TestQuery, ValidationResult
from src.services.test_query_service import TestQueryService
from src.services.validation_service import ValidationService

logger = logging.getLogger(__name__)


class TestExecutor:
    """Framework for executing validation tests"""

    def __init__(self):
        self.test_query_service = TestQueryService()

    def execute_single_test(self, test_query: TestQuery) -> ValidationResult:
        """Execute a single test and return validation result"""
        start_time = time.time()

        try:
            # Execute the test query
            result = self.test_query_service.execute_single_test_query(test_query)

            # Calculate success based on validation result
            success = result['validation_result'].success
            execution_time = time.time() - start_time

            return ValidationResult(
                query_id=test_query.query_text[:50] + "..." if len(test_query.query_text) > 50 else test_query.query_text,
                retrieved_chunks=result['results'],
                relevance_score=result['validation_result'].details.get('relevance_score', 0.0) if result['validation_result'].details else 0.0,
                metadata_accuracy=True,  # Assuming metadata is accurate for now
                response_time=execution_time,
                passed=success,
                timestamp=datetime.now()
            )
        except Exception as e:
            logger.error(f"Error executing test: {str(e)}", exc_info=True)
            execution_time = time.time() - start_time
            return ValidationResult(
                query_id=test_query.query_text[:50] + "..." if len(test_query.query_text) > 50 else test_query.query_text,
                retrieved_chunks=[],
                relevance_score=0.0,
                metadata_accuracy=False,
                response_time=execution_time,
                passed=False,
                timestamp=datetime.now()
            )

    def execute_test_suite(self, test_queries: List[TestQuery], suite_name: str = "Default Test Suite") -> Dict[str, Any]:
        """Execute a suite of tests and return comprehensive results"""
        start_time = time.time()

        results = []
        for i, test_query in enumerate(test_queries):
            logger.info(f"Executing test {i+1}/{len(test_queries)}: {test_query.query_text[:50]}...")
            result = self.execute_single_test(test_query)
            results.append(result)

        total_time = time.time() - start_time
        successful_tests = sum(1 for r in results if r.passed)
        success_rate = successful_tests / len(results) if results else 0

        # Calculate average response time
        avg_response_time = sum(r.response_time for r in results) / len(results) if results else 0

        return {
            'suite_name': suite_name,
            'total_tests': len(results),
            'successful_tests': successful_tests,
            'failed_tests': len(results) - successful_tests,
            'success_rate': success_rate,
            'total_execution_time': total_time,
            'average_response_time': avg_response_time,
            'results': results,
            'timestamp': datetime.now()
        }

    def execute_test_scenario(self, test_queries: List[TestQuery], scenario_name: str) -> Dict[str, Any]:
        """Execute a test scenario with additional reporting"""
        suite_result = self.execute_test_suite(test_queries, scenario_name)

        # Generate additional metrics for the scenario
        detailed_results = []
        for result in suite_result['results']:
            detailed_results.append({
                'query_id': result.query_id,
                'passed': result.passed,
                'relevance_score': result.relevance_score,
                'response_time': result.response_time,
                'retrieved_chunks_count': len(result.retrieved_chunks),
                'metadata_accuracy': result.metadata_accuracy
            })

        scenario_report = {
            **suite_result,
            'detailed_results': detailed_results,
            'pass_fail_breakdown': {
                'passed': [r for r in detailed_results if r['passed']],
                'failed': [r for r in detailed_results if not r['passed']]
            }
        }

        return scenario_report

    def run_predefined_scenarios(self) -> Dict[str, Any]:
        """Run all predefined test scenarios"""
        from src.validation.basic_search_scenarios import BasicSearchScenarios

        all_results = {}

        # Run AI robotics scenarios
        ai_robotics_tests = BasicSearchScenarios.get_ai_robotics_scenarios()
        all_results['ai_robotics'] = self.execute_test_scenario(ai_robotics_tests, "AI Robotics Scenarios")

        # Run humanoid movement scenarios
        humanoid_tests = BasicSearchScenarios.get_humanoid_movement_scenarios()
        all_results['humanoid_movement'] = self.execute_test_scenario(humanoid_tests, "Humanoid Movement Scenarios")

        # Run physical AI scenarios
        physical_ai_tests = BasicSearchScenarios.get_physical_ai_scenarios()
        all_results['physical_ai'] = self.execute_test_scenario(physical_ai_tests, "Physical AI Scenarios")

        # Run edge case scenarios
        edge_case_tests = BasicSearchScenarios.get_edge_case_scenarios()
        all_results['edge_cases'] = self.execute_test_scenario(edge_case_tests, "Edge Case Scenarios")

        # Run all scenarios together
        all_tests = BasicSearchScenarios.get_all_scenarios()
        all_results['all_scenarios'] = self.execute_test_scenario(all_tests, "All Scenarios")

        return all_results

    def generate_test_report(self, results: Dict[str, Any]) -> str:
        """Generate a human-readable test report"""
        report_lines = []
        report_lines.append("Test Execution Report")
        report_lines.append("=" * 50)

        for scenario_name, scenario_result in results.items():
            report_lines.append(f"\nScenario: {scenario_name}")
            report_lines.append(f"  Total Tests: {scenario_result['total_tests']}")
            report_lines.append(f"  Successful: {scenario_result['successful_tests']}")
            report_lines.append(f"  Failed: {scenario_result['failed_tests']}")
            report_lines.append(f"  Success Rate: {scenario_result['success_rate']:.2%}")
            report_lines.append(f"  Total Time: {scenario_result['total_execution_time']:.2f}s")
            report_lines.append(f"  Avg Response Time: {scenario_result['average_response_time']:.2f}s")

        report_lines.append(f"\nOverall Success Rate: {self._calculate_overall_success_rate(results):.2%}")
        report_lines.append(f"Total Execution Time: {self._calculate_total_execution_time(results):.2f}s")

        return "\n".join(report_lines)

    def _calculate_overall_success_rate(self, results: Dict[str, Any]) -> float:
        """Calculate overall success rate across all scenarios"""
        total_tests = 0
        successful_tests = 0

        for scenario_result in results.values():
            total_tests += scenario_result['total_tests']
            successful_tests += scenario_result['successful_tests']

        return successful_tests / total_tests if total_tests > 0 else 0

    def _calculate_total_execution_time(self, results: Dict[str, Any]) -> float:
        """Calculate total execution time across all scenarios"""
        return sum(scenario_result['total_execution_time'] for scenario_result in results.values())

    def validate_test_results(self, results: Dict[str, Any], expected_success_rate: float = 0.9) -> bool:
        """Validate that test results meet expected success criteria"""
        overall_success_rate = self._calculate_overall_success_rate(results)
        return overall_success_rate >= expected_success_rate

    def get_test_statistics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Get comprehensive statistics about test execution"""
        all_results = []
        for scenario_result in results.values():
            all_results.extend(scenario_result['results'])

        if not all_results:
            return {}

        # Calculate various statistics
        total_tests = len(all_results)
        successful_tests = sum(1 for r in all_results if r.passed)
        response_times = [r.response_time for r in all_results]
        relevance_scores = [r.relevance_score for r in all_results if r.relevance_score is not None]

        stats = {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'failed_tests': total_tests - successful_tests,
            'success_rate': successful_tests / total_tests if total_tests > 0 else 0,
            'response_time_stats': {
                'min': min(response_times) if response_times else 0,
                'max': max(response_times) if response_times else 0,
                'average': sum(response_times) / len(response_times) if response_times else 0,
                'total': sum(response_times) if response_times else 0
            },
            'relevance_score_stats': {
                'min': min(relevance_scores) if relevance_scores else 0,
                'max': max(relevance_scores) if relevance_scores else 0,
                'average': sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0
            }
        }

        return stats