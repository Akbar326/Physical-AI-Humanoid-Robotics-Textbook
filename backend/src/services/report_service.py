"""
Validation summary report service
"""

from typing import Dict, Any, List, Optional
import json
import csv
from datetime import datetime
from dataclasses import dataclass
import logging


logger = logging.getLogger(__name__)


@dataclass
class ValidationResultSummary:
    """Data class for validation result summary"""
    validation_id: str
    test_name: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    success_rate: float
    start_time: datetime
    end_time: datetime
    duration: float
    details: Optional[Dict[str, Any]] = None


class ReportService:
    """Service for generating validation summary reports"""

    def __init__(self):
        self.reports: List[Dict[str, Any]] = []

    def generate_validation_summary(self, validation_results: List[Dict[str, Any]],
                                   validation_name: str = "Validation Summary") -> Dict[str, Any]:
        """
        Generate a summary report from validation results

        Args:
            validation_results: List of validation results
            validation_name: Name for the validation summary

        Returns:
            Dictionary with validation summary
        """
        if not validation_results:
            return {
                'validation_name': validation_name,
                'total_results': 0,
                'summary': {},
                'timestamp': datetime.now().isoformat()
            }

        total_tests = len(validation_results)
        passed_tests = sum(1 for result in validation_results if result.get('passed', False))
        failed_tests = total_tests - passed_tests
        success_rate = passed_tests / total_tests if total_tests > 0 else 0

        # Calculate average response time
        response_times = [result.get('response_time', 0) for result in validation_results
                         if 'response_time' in result]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0

        # Calculate average relevance score
        relevance_scores = [result.get('relevance_score', 0) for result in validation_results
                           if 'relevance_score' in result]
        avg_relevance_score = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0

        # Group results by category
        category_results = {}
        for result in validation_results:
            category = result.get('category', 'uncategorized')
            if category not in category_results:
                category_results[category] = {
                    'total': 0,
                    'passed': 0,
                    'failed': 0
                }
            category_results[category]['total'] += 1
            if result.get('passed', False):
                category_results[category]['passed'] += 1
            else:
                category_results[category]['failed'] += 1

        # Calculate success rates by category
        for category in category_results:
            cat_data = category_results[category]
            cat_data['success_rate'] = cat_data['passed'] / cat_data['total'] if cat_data['total'] > 0 else 0

        summary = {
            'validation_name': validation_name,
            'total_results': total_tests,
            'passed_results': passed_tests,
            'failed_results': failed_tests,
            'success_rate': success_rate,
            'average_response_time': avg_response_time,
            'average_relevance_score': avg_relevance_score,
            'category_breakdown': category_results,
            'timestamp': datetime.now().isoformat(),
            'details': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'success_rate_percentage': success_rate * 100
            }
        }

        # Add to reports history
        self.reports.append(summary)

        return summary

    def generate_detailed_report(self, validation_results: List[Dict[str, Any]],
                                validation_name: str = "Detailed Validation Report") -> Dict[str, Any]:
        """
        Generate a detailed report with individual test results

        Args:
            validation_results: List of validation results
            validation_name: Name for the detailed report

        Returns:
            Dictionary with detailed validation report
        """
        summary = self.generate_validation_summary(validation_results, validation_name)

        detailed_results = []
        for i, result in enumerate(validation_results):
            detailed_result = {
                'index': i,
                'test_id': result.get('query_id', f'test_{i}'),
                'query': result.get('query', 'N/A'),
                'passed': result.get('passed', False),
                'relevance_score': result.get('relevance_score', 0),
                'response_time': result.get('response_time', 0),
                'metadata_accuracy': result.get('metadata_accuracy', False),
                'details': result.get('details', {}),
                'timestamp': result.get('timestamp', datetime.now().isoformat())
            }
            detailed_results.append(detailed_result)

        report = {
            **summary,
            'validation_name': validation_name,
            'detailed_results': detailed_results,
            'report_type': 'detailed'
        }

        return report

    def generate_reliability_report(self, reliability_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a reliability report from batch test results

        Args:
            reliability_results: Results from batch test execution

        Returns:
            Dictionary with reliability report
        """
        report = {
            'report_type': 'reliability',
            'validation_name': 'Reliability Test Report',
            'total_scenarios': reliability_results.get('total_scenarios', 0),
            'total_queries': reliability_results.get('total_queries', 0),
            'successful_queries': reliability_results.get('successful_queries', 0),
            'failed_queries': reliability_results.get('failed_queries', 0),
            'success_rate': reliability_results.get('success_rate', 0),
            'total_execution_time': reliability_results.get('total_execution_time', 0),
            'average_response_time': reliability_results.get('average_response_time', 0),
            'timestamp': datetime.now().isoformat()
        }

        # Add scenario-specific details
        scenario_results = reliability_results.get('results', [])
        scenario_details = []

        for scenario_result in scenario_results:
            scenario_detail = {
                'scenario_name': scenario_result.get('scenario_name', 'Unknown'),
                'scenario_description': scenario_result.get('scenario_description', ''),
                'total_queries': len(scenario_result.get('query_results', [])),
                'successful_queries': sum(1 for qr in scenario_result.get('query_results', [])
                                        if qr.get('validation_result', {}).get('passed', False)),
                'query_results_summary': [
                    {
                        'query': qr.get('query', {}).get('query_text', ''),
                        'passed': qr.get('validation_result', {}).get('passed', False),
                        'response_time': qr.get('execution_time', 0)
                    }
                    for qr in scenario_result.get('query_results', [])
                ]
            }
            scenario_detail['success_rate'] = (
                scenario_detail['successful_queries'] / scenario_detail['total_queries']
                if scenario_detail['total_queries'] > 0 else 0
            )
            scenario_details.append(scenario_detail)

        report['scenario_details'] = scenario_details

        return report

    def export_report_to_json(self, report: Dict[str, Any], filename: str = None) -> str:
        """
        Export a report to JSON format

        Args:
            report: The report to export
            filename: Optional filename for the export

        Returns:
            JSON string of the report
        """
        if filename is None:
            filename = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        json_content = json.dumps(report, indent=2, default=str)

        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json_content)

        logger.info(f"Report exported to {filename}")
        return json_content

    def export_report_to_csv(self, report: Dict[str, Any], filename: str = None) -> str:
        """
        Export a report to CSV format (for detailed results)

        Args:
            report: The report to export
            filename: Optional filename for the export

        Returns:
            Filename of the exported CSV
        """
        if filename is None:
            filename = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        detailed_results = report.get('detailed_results', [])

        if not detailed_results:
            logger.warning("No detailed results to export to CSV")
            return ""

        fieldnames = detailed_results[0].keys() if detailed_results else ['No data']

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in detailed_results:
                writer.writerow(result)

        logger.info(f"Report exported to {filename}")
        return filename

    def generate_metadata_validation_report(self, metadata_validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a report specifically for metadata validation

        Args:
            metadata_validation_results: Results from metadata validation

        Returns:
            Dictionary with metadata validation report
        """
        if not metadata_validation_results:
            return {
                'report_type': 'metadata_validation',
                'validation_name': 'Metadata Validation Report',
                'total_results': 0,
                'summary': {},
                'timestamp': datetime.now().isoformat()
            }

        # Calculate metadata validation statistics
        total_results = len(metadata_validation_results)
        valid_results = sum(1 for result in metadata_validation_results
                           if result.get('overall_valid', False))
        invalid_results = total_results - valid_results
        metadata_accuracy = valid_results / total_results if total_results > 0 else 0

        # Extract metadata validation details
        completeness_validation_results = [
            result.get('completeness_validation', {})
            for result in metadata_validation_results
        ]

        # Count completeness validation results
        completeness_passed = sum(1 for result in completeness_validation_results
                                 if result.get('success', False))

        accuracy_validation_results = [
            result.get('accuracy_validation', {})
            for result in metadata_validation_results
        ]

        # Count accuracy validation results
        accuracy_passed = sum(1 for result in accuracy_validation_results
                             if result.get('success', False))

        report = {
            'report_type': 'metadata_validation',
            'validation_name': 'Metadata Validation Report',
            'total_results': total_results,
            'valid_results': valid_results,
            'invalid_results': invalid_results,
            'metadata_accuracy': metadata_accuracy,
            'completeness_validation_passed': completeness_passed,
            'accuracy_validation_passed': accuracy_passed,
            'completeness_validation_rate': completeness_passed / total_results if total_results > 0 else 0,
            'accuracy_validation_rate': accuracy_passed / total_results if total_results > 0 else 0,
            'timestamp': datetime.now().isoformat(),
            'details': {
                'total_results': total_results,
                'valid_results': valid_results,
                'invalid_results': invalid_results,
                'metadata_accuracy_percentage': metadata_accuracy * 100
            }
        }

        return report

    def generate_comparison_report(self, baseline_results: List[Dict[str, Any]],
                                  current_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a comparison report between baseline and current validation results

        Args:
            baseline_results: Baseline validation results
            current_results: Current validation results

        Returns:
            Dictionary with comparison report
        """
        baseline_summary = self.generate_validation_summary(baseline_results, "Baseline")
        current_summary = self.generate_validation_summary(current_results, "Current")

        # Calculate differences
        success_rate_diff = current_summary['success_rate'] - baseline_summary['success_rate']
        avg_response_time_diff = current_summary['average_response_time'] - baseline_summary['average_response_time']
        avg_relevance_diff = current_summary['average_relevance_score'] - baseline_summary['average_relevance_score']

        comparison_report = {
            'report_type': 'comparison',
            'validation_name': 'Baseline vs Current Comparison Report',
            'baseline_summary': baseline_summary,
            'current_summary': current_summary,
            'differences': {
                'success_rate_change': success_rate_diff,
                'success_rate_change_percentage': success_rate_diff * 100,
                'response_time_change': avg_response_time_diff,
                'relevance_score_change': avg_relevance_diff
            },
            'improvement': {
                'success_rate_improved': success_rate_diff > 0,
                'response_time_improved': avg_response_time_diff < 0,  # Lower is better
                'relevance_improved': avg_relevance_diff > 0
            },
            'timestamp': datetime.now().isoformat()
        }

        return comparison_report

    def get_report_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of generated reports

        Returns:
            List of previously generated reports
        """
        return self.reports

    def generate_executive_summary(self, validation_results: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Generate an executive summary of validation results

        Args:
            validation_results: List of validation results

        Returns:
            Dictionary with executive summary
        """
        summary = self.generate_validation_summary(validation_results)

        success_rate = summary['success_rate']
        avg_response_time = summary['average_response_time']
        avg_relevance_score = summary['average_relevance_score']

        # Generate textual summary
        status = "EXCELLENT" if success_rate >= 0.95 else "GOOD" if success_rate >= 0.90 else "FAIR" if success_rate >= 0.80 else "POOR"

        executive_summary = {
            'status': status,
            'success_rate': f"{success_rate * 100:.2f}%",
            'average_response_time': f"{avg_response_time:.2f}s",
            'average_relevance_score': f"{avg_relevance_score:.2f}",
            'total_tests': str(summary['total_results']),
            'passed_tests': str(summary['passed_results']),
            'failed_tests': str(summary['failed_results']),
            'summary_text': (
                f"The validation pipeline performed {status.lower()} with a {success_rate * 100:.1f}% "
                f"success rate. Average response time was {avg_response_time:.2f}s and average "
                f"relevance score was {avg_relevance_score:.2f}. "
                f"Out of {summary['total_results']} tests, {summary['passed_results']} passed "
                f"and {summary['failed_results']} failed."
            )
        }

        return executive_summary

    def save_report(self, report: Dict[str, Any], report_name: str) -> str:
        """
        Save a report with a specific name

        Args:
            report: The report to save
            report_name: Name to save the report as

        Returns:
            Path where the report was saved
        """
        filename = f"validation_report_{report_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.export_report_to_json(report, filename)
        return filename