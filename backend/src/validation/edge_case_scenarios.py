"""
Edge case test scenarios for validation
"""

from typing import List
from src.models.validation import TestScenario, ValidationCriterion, TestQuery


class EdgeCaseScenarios:
    """Test scenarios for edge cases in the validation system"""

    def get_empty_query_scenarios(self) -> List[TestScenario]:
        """Get scenarios for testing empty or minimal queries"""
        scenarios = [
            TestScenario(
                name="Empty Query Test",
                description="Test behavior when query is empty",
                queries=[
                    TestQuery(
                        query_text="",
                        expected_concepts=[],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Empty Query Handling",
                        description="System should handle empty queries gracefully without crashing",
                        threshold=1.0,
                        metric="error_handling"
                    )
                ],
                category="error_handling"
            ),
            TestScenario(
                name="Whitespace Query Test",
                description="Test behavior when query contains only whitespace",
                queries=[
                    TestQuery(
                        query_text="   ",
                        expected_concepts=[],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Whitespace Query Handling",
                        description="System should handle whitespace-only queries gracefully",
                        threshold=1.0,
                        metric="error_handling"
                    )
                ],
                category="error_handling"
            )
        ]

        return scenarios

    def get_extreme_length_scenarios(self) -> List[TestScenario]:
        """Get scenarios for testing very short and very long queries"""
        scenarios = [
            TestScenario(
                name="Single Character Query Test",
                description="Test behavior with single character query",
                queries=[
                    TestQuery(
                        query_text="A",
                        expected_concepts=["A"],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Single Character Handling",
                        description="System should handle single character queries",
                        threshold=0.8,
                        metric="success_rate"
                    )
                ],
                category="extreme_length"
            ),
            TestScenario(
                name="Very Long Query Test",
                description="Test behavior with very long query string",
                queries=[
                    TestQuery(
                        query_text="Artificial intelligence and machine learning and deep learning and neural networks and "
                                  "computer vision and natural language processing and robotics and automation and "
                                  "data science and big data and cloud computing and distributed systems and "
                                  "algorithm design and computational complexity and software engineering and "
                                  "computer architecture and operating systems and database systems and "
                                  "cybersecurity and cryptography and human computer interaction and computer graphics and "
                                  "mobile computing and internet of things and blockchain technology and quantum computing",
                        expected_concepts=["artificial intelligence", "machine learning", "deep learning", "neural networks"],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Long Query Handling",
                        description="System should handle very long queries without performance degradation",
                        threshold=0.8,
                        metric="success_rate"
                    ),
                    ValidationCriterion(
                        name="Long Query Response Time",
                        description="Response time for long queries should be reasonable",
                        threshold=10.0,  # 10 seconds max
                        metric="response_time"
                    )
                ],
                category="extreme_length"
            )
        ]

        return scenarios

    def get_special_character_scenarios(self) -> List[TestScenario]:
        """Get scenarios for testing queries with special characters"""
        scenarios = [
            TestScenario(
                name="Special Characters Query Test",
                description="Test behavior with queries containing special characters",
                queries=[
                    TestQuery(
                        query_text="AI's & robotics: future implications?",
                        expected_concepts=["AI", "robotics", "future", "implications"],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Special Character Handling",
                        description="System should handle special characters correctly",
                        threshold=0.9,
                        metric="success_rate"
                    )
                ],
                category="special_characters"
            ),
            TestScenario(
                name="Unicode Query Test",
                description="Test behavior with queries containing Unicode characters",
                queries=[
                    TestQuery(
                        query_text="Artificial Intelligence (AI) 人工知能",
                        expected_concepts=["artificial intelligence", "AI"],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Unicode Handling",
                        description="System should handle Unicode characters correctly",
                        threshold=0.85,
                        metric="success_rate"
                    )
                ],
                category="special_characters"
            )
        ]

        return scenarios

    def get_no_result_scenarios(self) -> List[TestScenario]:
        """Get scenarios for testing queries that might return no results"""
        scenarios = [
            TestScenario(
                name="Uncommon Term Query Test",
                description="Test behavior with very uncommon or made-up terms",
                queries=[
                    TestQuery(
                        query_text="xyzzyx quasar quantum mechanics",
                        expected_concepts=["xyzzyx", "quasar", "quantum mechanics"],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="No Result Handling",
                        description="System should handle queries with no results gracefully",
                        threshold=1.0,
                        metric="error_handling"
                    )
                ],
                category="no_results"
            ),
            TestScenario(
                name="Nonsense Query Test",
                description="Test behavior with completely nonsensical queries",
                queries=[
                    TestQuery(
                        query_text="flibbertigibbet wobblewockle",
                        expected_concepts=[],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Nonsense Query Handling",
                        description="System should handle nonsensical queries without crashing",
                        threshold=1.0,
                        metric="error_handling"
                    )
                ],
                category="no_results"
            )
        ]

        return scenarios

    def get_concurrency_scenarios(self) -> List[TestScenario]:
        """Get scenarios for testing concurrent queries"""
        scenarios = [
            TestScenario(
                name="Rapid Fire Queries Test",
                description="Test behavior when multiple queries are made rapidly",
                queries=[
                    TestQuery(
                        query_text="AI",
                        expected_concepts=["artificial intelligence"],
                        category="edge_cases"
                    ),
                    TestQuery(
                        query_text="robotics",
                        expected_concepts=["robotics"],
                        category="edge_cases"
                    ),
                    TestQuery(
                        query_text="machine learning",
                        expected_concepts=["machine learning"],
                        category="edge_cases"
                    ),
                    TestQuery(
                        query_text="neural networks",
                        expected_concepts=["neural networks"],
                        category="edge_cases"
                    ),
                    TestQuery(
                        query_text="computer vision",
                        expected_concepts=["computer vision"],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Rapid Query Handling",
                        description="System should handle rapid queries without errors",
                        threshold=0.9,
                        metric="success_rate"
                    ),
                    ValidationCriterion(
                        name="Concurrency Stability",
                        description="System should remain stable under rapid query load",
                        threshold=0.95,
                        metric="stability"
                    )
                ],
                category="concurrency"
            )
        ]

        return scenarios

    def get_error_handling_scenarios(self) -> List[TestScenario]:
        """Get scenarios for testing error conditions"""
        scenarios = [
            TestScenario(
                name="Network Timeout Simulation",
                description="Test behavior when external services timeout",
                queries=[
                    TestQuery(
                        query_text="External API query that might timeout",
                        expected_concepts=["API", "timeout"],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Timeout Handling",
                        description="System should handle timeouts gracefully",
                        threshold=1.0,
                        metric="error_handling"
                    )
                ],
                category="error_handling"
            ),
            TestScenario(
                name="Malformed Query Test",
                description="Test behavior with intentionally malformed queries",
                queries=[
                    TestQuery(
                        query_text="SELECT * FROM users WHERE password=' OR '1'='1",
                        expected_concepts=["malformed", "security"],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Malformed Query Handling",
                        description="System should handle potentially malicious queries safely",
                        threshold=1.0,
                        metric="security_handling"
                    )
                ],
                category="security"
            )
        ]

        return scenarios

    def get_all_edge_case_scenarios(self) -> List[TestScenario]:
        """Get all edge case test scenarios"""
        all_scenarios = []
        all_scenarios.extend(self.get_empty_query_scenarios())
        all_scenarios.extend(self.get_extreme_length_scenarios())
        all_scenarios.extend(self.get_special_character_scenarios())
        all_scenarios.extend(self.get_no_result_scenarios())
        all_scenarios.extend(self.get_concurrency_scenarios())
        all_scenarios.extend(self.get_error_handling_scenarios())

        return all_scenarios