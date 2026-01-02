"""
Metadata validation test scenarios
"""

from typing import List, Dict, Any
from src.models.validation import TestScenario, ValidationCriterion, TestQuery
from src.services.metadata_service import MetadataService


class MetadataScenarios:
    """Test scenarios for metadata validation"""

    def __init__(self):
        self.metadata_service = MetadataService()

    def get_basic_metadata_scenarios(self) -> List[TestScenario]:
        """Get basic metadata validation scenarios"""
        scenarios = [
            TestScenario(
                name="URL Format Validation",
                description="Validate that URLs in search results have correct format",
                queries=[
                    TestQuery(
                        query_text="AI robotics fundamentals",
                        expected_concepts=["artificial intelligence", "robotics"],
                        category="ai_robotics"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="URL Format Check",
                        description="URLs must start with http:// or https://",
                        threshold=1.0,
                        metric="format_validation"
                    )
                ],
                category="P1"
            ),
            TestScenario(
                name="Chunk ID Validation",
                description="Validate that chunk IDs are properly formatted and unique",
                queries=[
                    TestQuery(
                        query_text="Humanoid robot movement",
                        expected_concepts=["humanoid", "movement", "kinematics"],
                        category="humanoid_robotics"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Chunk ID Format Check",
                        description="Chunk IDs must be non-empty strings",
                        threshold=1.0,
                        metric="format_validation"
                    )
                ],
                category="P1"
            ),
            TestScenario(
                name="Content Metadata Validation",
                description="Validate that content metadata is properly extracted and complete",
                queries=[
                    TestQuery(
                        query_text="Physical AI principles",
                        expected_concepts=["physical AI", "principles", "embodied intelligence"],
                        category="physical_ai"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Content Length Check",
                        description="Content must have non-zero length",
                        threshold=0.5,
                        metric="length_validation"
                    ),
                    ValidationCriterion(
                        name="Content Completeness Check",
                        description="Content must contain meaningful text",
                        threshold=0.5,
                        metric="completeness_validation"
                    )
                ],
                category="P1"
            )
        ]

        return scenarios

    def get_advanced_metadata_scenarios(self) -> List[TestScenario]:
        """Get advanced metadata validation scenarios"""
        scenarios = [
            TestScenario(
                name="URL Accessibility Validation",
                description="Validate that source URLs in search results are accessible",
                queries=[
                    TestQuery(
                        query_text="AI robotics research papers",
                        expected_concepts=["research", "papers", "AI", "robotics"],
                        category="ai_robotics"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="URL Accessibility Check",
                        description="Source URLs must return 200 status when accessed",
                        threshold=1.0,
                        metric="accessibility_validation"
                    )
                ],
                category="P2"
            ),
            TestScenario(
                name="Metadata Consistency Validation",
                description="Validate that metadata is consistent across multiple search results",
                queries=[
                    TestQuery(
                        query_text="Humanoid locomotion techniques",
                        expected_concepts=["locomotion", "techniques", "humanoid"],
                        category="humanoid_robotics"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Metadata Consistency Check",
                        description="All results should have consistent metadata fields",
                        threshold=1.0,
                        metric="consistency_validation"
                    )
                ],
                category="P2"
            ),
            TestScenario(
                name="Email and URL Extraction Validation",
                description="Validate that emails and URLs are properly extracted from content",
                queries=[
                    TestQuery(
                        query_text="AI robotics documentation",
                        expected_concepts=["documentation", "API", "references"],
                        category="documentation"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Email Extraction Check",
                        description="Content should have properly formatted emails extracted",
                        threshold=0.5,
                        metric="extraction_validation"
                    ),
                    ValidationCriterion(
                        name="URL Extraction Check",
                        description="Content should have properly formatted URLs extracted",
                        threshold=0.5,
                        metric="extraction_validation"
                    )
                ],
                category="P2"
            )
        ]

        return scenarios

    def get_edge_case_metadata_scenarios(self) -> List[TestScenario]:
        """Get edge case metadata validation scenarios"""
        scenarios = [
            TestScenario(
                name="Empty Metadata Validation",
                description="Validate behavior when metadata fields are missing or empty",
                queries=[
                    TestQuery(
                        query_text="edge case query",
                        expected_concepts=["edge", "case"],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Empty Field Handling",
                        description="System should handle empty metadata fields gracefully",
                        threshold=1.0,
                        metric="error_handling_validation"
                    )
                ],
                category="P3"
            ),
            TestScenario(
                name="Invalid Format Validation",
                description="Validate behavior with invalid metadata formats",
                queries=[
                    TestQuery(
                        query_text="invalid format test",
                        expected_concepts=["invalid", "format"],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Invalid Format Handling",
                        description="System should handle invalid formats gracefully",
                        threshold=1.0,
                        metric="format_validation"
                    )
                ],
                category="P3"
            )
        ]

        return scenarios

    def get_all_metadata_scenarios(self) -> List[TestScenario]:
        """Get all metadata validation scenarios"""
        all_scenarios = []
        all_scenarios.extend(self.get_basic_metadata_scenarios())
        all_scenarios.extend(self.get_advanced_metadata_scenarios())
        all_scenarios.extend(self.get_edge_case_metadata_scenarios())

        return all_scenarios