"""
End-to-end validation pipeline tests
"""

import unittest
import os
from src.services.search_service import SearchService
from src.services.metadata_service import MetadataService
from src.services.validation_service import ValidationService
from src.services.batch_test_service import BatchTestService
from src.services.performance_monitor import PerformanceMonitor
from src.validation.reliability_scenarios import ReliabilityScenarios
from src.validation.edge_case_scenarios import EdgeCaseScenarios
from src.services.error_handler import ErrorHandler
from src.services.logging_service import ValidationLoggingService
from src.services.report_service import ReportService
from src.services.performance_optimizer import PerformanceOptimizer


class TestEndToEndValidationPipeline(unittest.TestCase):
    """End-to-end tests for the complete validation pipeline"""

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
        self.search_service = SearchService()
        self.metadata_service = MetadataService()
        self.batch_test_service = BatchTestService()
        self.performance_monitor = PerformanceMonitor()
        self.error_handler = ErrorHandler()
        self.validation_logger = ValidationLoggingService()
        self.report_service = ReportService()
        self.performance_optimizer = PerformanceOptimizer()
        self.reliability_scenarios = ReliabilityScenarios()
        self.edge_case_scenarios = EdgeCaseScenarios()

    def test_complete_validation_pipeline(self):
        """Test the complete validation pipeline from search to reporting"""
        validation_id = "e2e_test_complete_pipeline"

        # Start performance monitoring
        start_time = self.performance_monitor.start_timer()

        # Log the start of validation
        self.validation_logger.log_validation_start(validation_id, "Starting complete validation pipeline")

        try:
            # Step 1: Perform a search
            query_text = "AI robotics fundamentals"
            self.validation_logger.log_validation_step(validation_id, "search", f"Searching for: {query_text}")

            search_results = self.search_service.search(query_text, top_k=3)
            self.validation_logger.log_validation_result(validation_id, len(search_results), len(search_results) > 0)

            # Step 2: Validate metadata for search results
            self.validation_logger.log_validation_step(validation_id, "metadata_validation", "Validating metadata")

            metadata_validation_results = self.metadata_service.validate_search_result_metadata(search_results)
            metadata_summary = self.metadata_service.get_metadata_summary(search_results)

            self.validation_logger.log_validation_result(
                validation_id,
                f"Metadata validation results: {len(metadata_validation_results)}",
                True
            )

            # Step 3: Generate a report
            self.validation_logger.log_validation_step(validation_id, "report_generation", "Generating validation report")

            report = self.report_service.generate_validation_summary(
                metadata_validation_results,
                "E2E Validation Report"
            )

            self.validation_logger.log_validation_result(validation_id, "Report generated", True)

            # Step 4: Check success criteria
            success_rate = report.get('success_rate', 0)
            self.assertGreaterEqual(success_rate, 0.8, f"Success rate {success_rate} is below threshold of 0.8")

            # Step 5: Log completion
            response_time = self.performance_monitor.end_timer(start_time, "complete_validation_pipeline", True)
            self.validation_logger.log_performance_metric(validation_id, "total_response_time", response_time)
            self.validation_logger.log_validation_end(validation_id, response_time, True)

            # Step 6: Verify report contents
            self.assertIn('total_results', report)
            self.assertIn('passed_results', report)
            self.assertIn('failed_results', report)
            self.assertIn('success_rate', report)

        except Exception as e:
            # Log error and end validation
            response_time = self.performance_monitor.end_timer(start_time, "complete_validation_pipeline", False)
            self.validation_logger.log_error(validation_id, e)
            self.validation_logger.log_validation_end(validation_id, response_time, False)
            raise

    @unittest.skipIf(not (TestEndToEndValidationPipeline.has_cohere_key and TestEndToEndValidationPipeline.has_qdrant_config),
                     "Missing required environment configuration for end-to-end tests")
    def test_batch_reliability_validation(self):
        """Test batch reliability validation across multiple scenarios"""
        validation_id = "e2e_test_batch_reliability"

        # Start performance monitoring
        start_time = self.performance_monitor.start_timer()
        self.validation_logger.log_validation_start(validation_id, "Starting batch reliability validation")

        try:
            # Get reliability scenarios
            scenarios = self.reliability_scenarios.get_basic_reliability_scenarios()
            self.assertGreater(len(scenarios), 0, "No reliability scenarios found")

            # Execute batch tests
            batch_results = self.batch_test_service.execute_batch_tests(scenarios, max_concurrent=3)

            self.validation_logger.log_validation_result(
                validation_id,
                f"Batch test results: {batch_results['total_queries']} queries",
                True
            )

            # Generate reliability report
            reliability_report = self.report_service.generate_reliability_report(batch_results)
            self.validation_logger.log_validation_step(validation_id, "reliability_report", "Generated reliability report")

            # Verify reliability criteria
            success_rate = batch_results.get('success_rate', 0)
            self.assertGreaterEqual(success_rate, 0.8, f"Batch success rate {success_rate} is below threshold")

            # Validate response time
            avg_response_time = batch_results.get('average_response_time', float('inf'))
            self.assertLess(avg_response_time, 10.0, f"Average response time {avg_response_time}s is too high")

            # End validation
            response_time = self.performance_monitor.end_timer(start_time, "batch_reliability_validation", True)
            self.validation_logger.log_performance_metric(validation_id, "total_response_time", response_time)
            self.validation_logger.log_validation_end(validation_id, response_time, True)

        except Exception as e:
            response_time = self.performance_monitor.end_timer(start_time, "batch_reliability_validation", False)
            self.validation_logger.log_error(validation_id, e)
            self.validation_logger.log_validation_end(validation_id, response_time, False)
            raise

    @unittest.skipIf(not (TestEndToEndValidationPipeline.has_cohere_key and TestEndToEndValidationPipeline.has_qdrant_config),
                     "Missing required environment configuration for end-to-end tests")
    def test_edge_case_validation_pipeline(self):
        """Test validation pipeline with edge cases"""
        validation_id = "e2e_test_edge_case"

        # Start performance monitoring
        start_time = self.performance_monitor.start_timer()
        self.validation_logger.log_validation_start(validation_id, "Starting edge case validation")

        try:
            # Get edge case scenarios
            scenarios = self.edge_case_scenarios.get_all_edge_case_scenarios()
            self.assertGreater(len(scenarios), 0, "No edge case scenarios found")

            # Test with a simple query first to ensure basic functionality
            basic_query = "AI"
            search_results = self.search_service.search(basic_query, top_k=2)

            self.validation_logger.log_validation_result(
                validation_id,
                f"Basic search results: {len(search_results)}",
                len(search_results) > 0
            )

            # Validate metadata for basic results
            metadata_results = self.metadata_service.validate_search_result_metadata(search_results)
            metadata_summary = self.metadata_service.get_metadata_summary(search_results)

            # Generate edge case report
            edge_case_report = self.report_service.generate_metadata_validation_report(metadata_results)
            self.validation_logger.log_validation_step(validation_id, "edge_case_report", "Generated edge case report")

            # Verify edge case handling
            success_rate = edge_case_report.get('metadata_accuracy', 0)
            self.assertGreaterEqual(success_rate, 0.7, f"Edge case success rate {success_rate} is below threshold")

            # End validation
            response_time = self.performance_monitor.end_timer(start_time, "edge_case_validation", True)
            self.validation_logger.log_performance_metric(validation_id, "total_response_time", response_time)
            self.validation_logger.log_validation_end(validation_id, response_time, True)

        except Exception as e:
            response_time = self.performance_monitor.end_timer(start_time, "edge_case_validation", False)
            self.validation_logger.log_error(validation_id, e)
            self.validation_logger.log_validation_end(validation_id, response_time, False)
            raise

    def test_error_handling_in_validation_pipeline(self):
        """Test error handling throughout the validation pipeline"""
        validation_id = "e2e_test_error_handling"

        # Start performance monitoring
        start_time = self.performance_monitor.start_timer()
        self.validation_logger.log_validation_start(validation_id, "Starting error handling test")

        try:
            # Test with a potentially problematic query
            query_text = ""  # Empty query to test error handling

            # Use error handler to safely execute search
            search_results = self.error_handler.safe_execute(
                self.search_service.search,
                query_text,
                default_return=[],
                error_type=None,
                severity=None,
                context={'query': query_text}
            )

            self.validation_logger.log_validation_result(
                validation_id,
                f"Search results with error handling: {len(search_results)}",
                True  # Error handling itself is successful
            )

            # Test metadata validation with empty results
            metadata_results = self.metadata_service.validate_search_result_metadata(search_results)
            metadata_summary = self.metadata_service.get_metadata_summary(search_results)

            # Generate report even with minimal data
            report = self.report_service.generate_validation_summary(
                metadata_results,
                "Error Handling Validation Report"
            )

            # Verify that error handling worked properly
            error_summary = self.error_handler.get_error_summary()
            self.assertIn('total_errors', error_summary)

            # End validation
            response_time = self.performance_monitor.end_timer(start_time, "error_handling_validation", True)
            self.validation_logger.log_performance_metric(validation_id, "total_response_time", response_time)
            self.validation_logger.log_validation_end(validation_id, response_time, True)

        except Exception as e:
            response_time = self.performance_monitor.end_timer(start_time, "error_handling_validation", False)
            self.validation_logger.log_error(validation_id, e)
            self.validation_logger.log_validation_end(validation_id, response_time, False)
            raise

    @unittest.skipIf(not (TestEndToEndValidationPipeline.has_cohere_key and TestEndToEndValidationPipeline.has_qdrant_config),
                     "Missing required environment configuration for end-to-end tests")
    def test_performance_optimization_validation(self):
        """Test validation pipeline with performance optimization"""
        validation_id = "e2e_test_performance_optimization"

        # Start performance monitoring
        start_time = self.performance_monitor.start_timer()
        self.validation_logger.log_validation_start(validation_id, "Starting performance optimization test")

        try:
            # Run initial validation to get baseline
            query_text = "machine learning algorithms"
            search_results = self.search_service.search(query_text, top_k=3)

            # Validate results
            metadata_results = self.metadata_service.validate_search_result_metadata(search_results)
            initial_report = self.report_service.generate_validation_summary(
                metadata_results,
                "Initial Performance Report"
            )

            # Analyze results for optimization recommendations
            optimization_recommendations = self.performance_optimizer.analyze_validation_results(metadata_results)
            self.validation_logger.log_validation_step(
                validation_id,
                "optimization_analysis",
                f"Generated {len(optimization_recommendations)} recommendations"
            )

            # Apply high priority optimizations
            applied_optimizations = self.performance_optimizer.auto_optimize(metadata_results, max_recommendations=2)
            self.validation_logger.log_validation_result(
                validation_id,
                f"Applied {len(applied_optimizations)} optimizations",
                True
            )

            # Run validation again to see improvement
            search_results_after = self.search_service.search(query_text, top_k=3)
            metadata_results_after = self.metadata_service.validate_search_result_metadata(search_results_after)
            final_report = self.report_service.generate_validation_summary(
                metadata_results_after,
                "Final Performance Report"
            )

            # Generate comparison report
            comparison_report = self.report_service.generate_comparison_report(
                metadata_results,
                metadata_results_after
            )

            # Verify that optimization process completed
            self.assertIn('differences', comparison_report)
            self.assertIn('improvement', comparison_report)

            # End validation
            response_time = self.performance_monitor.end_timer(start_time, "performance_optimization_validation", True)
            self.validation_logger.log_performance_metric(validation_id, "total_response_time", response_time)
            self.validation_logger.log_validation_end(validation_id, response_time, True)

        except Exception as e:
            response_time = self.performance_monitor.end_timer(start_time, "performance_optimization_validation", False)
            self.validation_logger.log_error(validation_id, e)
            self.validation_logger.log_validation_end(validation_id, response_time, False)
            raise

    def test_complete_pipeline_without_external_services(self):
        """Test validation pipeline components without external services"""
        validation_id = "e2e_test_internal_components"

        # Start performance monitoring
        start_time = self.performance_monitor.start_timer()
        self.validation_logger.log_validation_start(validation_id, "Testing internal components without external services")

        try:
            # Test metadata service with sample data
            sample_content = "This is sample content for testing metadata extraction. Visit https://example.com for more info."
            sample_url = "https://test-source.com"

            extracted_metadata = self.metadata_service.extract_metadata_from_content(sample_content, sample_url)
            self.validation_logger.log_validation_result(
                validation_id,
                f"Extracted metadata fields: {list(extracted_metadata.keys())}",
                True
            )

            # Test metadata validation
            validation_result = self.metadata_service.validate_result_metadata(
                "test_chunk_1",
                sample_content,
                sample_url
            )
            self.validation_logger.log_validation_result(
                validation_id,
                f"Validation result overall valid: {validation_result['overall_valid']}",
                True
            )

            # Test report generation with sample data
            sample_validation_results = [
                {
                    'overall_valid': True,
                    'passed': True,
                    'response_time': 0.1,
                    'relevance_score': 0.9
                }
            ]
            report = self.report_service.generate_validation_summary(sample_validation_results)
            self.validation_logger.log_validation_result(
                validation_id,
                "Generated sample report",
                True
            )

            # Test error handling with mock error
            try:
                raise ValueError("Test error for error handling validation")
            except ValueError as e:
                handled_error = self.error_handler.handle_error(e)
                self.validation_logger.log_validation_result(
                    validation_id,
                    f"Handled error type: {handled_error.error_type}",
                    True
                )

            # End validation
            response_time = self.performance_monitor.end_timer(start_time, "internal_components_validation", True)
            self.validation_logger.log_performance_metric(validation_id, "total_response_time", response_time)
            self.validation_logger.log_validation_end(validation_id, response_time, True)

            # Verify all components worked
            self.assertIn('content_length', extracted_metadata)
            self.assertIn('contains_urls', extracted_metadata)
            self.assertTrue(validation_result['overall_valid'])
            self.assertIn('success_rate', report)

        except Exception as e:
            response_time = self.performance_monitor.end_timer(start_time, "internal_components_validation", False)
            self.validation_logger.log_error(validation_id, e)
            self.validation_logger.log_validation_end(validation_id, response_time, False)
            raise


class TestValidationPipelineIntegration(unittest.TestCase):
    """Integration tests for validation pipeline components"""

    def setUp(self):
        """Set up test fixtures"""
        self.search_service = SearchService()
        self.metadata_service = MetadataService()
        self.report_service = ReportService()
        self.performance_monitor = PerformanceMonitor()
        self.validation_logger = ValidationLoggingService()

    def test_service_integration(self):
        """Test integration between all validation services"""
        validation_id = "integration_test_all_services"

        start_time = self.performance_monitor.start_timer()
        self.validation_logger.log_validation_start(validation_id, "Testing service integration")

        try:
            # Create sample data
            sample_results = [
                {
                    'chunk_id': 'chunk_1',
                    'content': 'Sample content for integration testing',
                    'source_url': 'https://example.com',
                    'relevance_score': 0.85,
                    'position': 1
                }
            ]

            # Process through metadata service
            metadata_validation = self.metadata_service.validate_search_result_metadata(sample_results)
            summary = self.metadata_service.get_metadata_summary(sample_results)

            # Generate report
            report = self.report_service.generate_validation_summary(metadata_validation)

            # Log performance metrics
            self.performance_monitor.log_performance_metric(
                validation_id,
                "integration_processing_time",
                self.performance_monitor.end_timer(start_time, "integration_processing", True)
            )

            # Verify integration
            self.assertGreater(len(metadata_validation), 0)
            self.assertIn('success_rate', report)
            self.assertIn('total_results', summary)

            self.validation_logger.log_validation_end(validation_id, 0, True)

        except Exception as e:
            self.performance_monitor.end_timer(start_time, "integration_processing", False)
            self.validation_logger.log_error(validation_id, e)
            self.validation_logger.log_validation_end(validation_id, 0, False)
            raise


if __name__ == '__main__':
    unittest.main()