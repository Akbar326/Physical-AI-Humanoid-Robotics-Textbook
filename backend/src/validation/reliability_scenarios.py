"""
Reliability test scenarios for validation
"""

from typing import List
from src.models.validation import TestScenario, ValidationCriterion, TestQuery


class ReliabilityScenarios:
    """Test scenarios for reliability validation"""

    def get_basic_reliability_scenarios(self) -> List[TestScenario]:
        """Get basic reliability test scenarios"""
        scenarios = [
            TestScenario(
                name="Consistency Test",
                description="Test that the same query returns consistent results over multiple executions",
                queries=[
                    TestQuery(
                        query_text="AI robotics fundamentals",
                        expected_concepts=["artificial intelligence", "robotics", "AI"],
                        category="ai_robotics"
                    ),
                    TestQuery(
                        query_text="Humanoid robot locomotion",
                        expected_concepts=["humanoid", "locomotion", "movement"],
                        category="humanoid_robotics"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Consistency Check",
                        description="Results should be consistent across multiple runs",
                        threshold=0.9,
                        metric="consistency_rate"
                    )
                ],
                category="reliability"
            ),
            TestScenario(
                name="Performance Stability Test",
                description="Test that response times remain stable over multiple queries",
                queries=[
                    TestQuery(
                        query_text="Machine learning algorithms",
                        expected_concepts=["machine learning", "algorithms", "ML"],
                        category="ml"
                    ),
                    TestQuery(
                        query_text="Computer vision applications",
                        expected_concepts=["computer vision", "image processing", "CV"],
                        category="cv"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Performance Stability",
                        description="Average response time should be under 3 seconds",
                        threshold=3.0,
                        metric="average_response_time"
                    )
                ],
                category="reliability"
            )
        ]

        return scenarios

    def get_load_test_scenarios(self) -> List[TestScenario]:
        """Get scenarios for load testing"""
        scenarios = [
            TestScenario(
                name="High Volume Query Test",
                description="Test system performance under high query volume",
                queries=[
                    TestQuery(
                        query_text="AI ethics principles",
                        expected_concepts=["AI ethics", "ethics", "principles"],
                        category="ai_ethics"
                    ),
                    TestQuery(
                        query_text="Neural network architectures",
                        expected_concepts=["neural networks", "architectures", "deep learning"],
                        category="deep_learning"
                    ),
                    TestQuery(
                        query_text="Reinforcement learning methods",
                        expected_concepts=["reinforcement learning", "RL", "methods"],
                        category="rl"
                    ),
                    TestQuery(
                        query_text="Natural language processing",
                        expected_concepts=["NLP", "natural language", "processing"],
                        category="nlp"
                    ),
                    TestQuery(
                        query_text="Computer vision fundamentals",
                        expected_concepts=["computer vision", "CV", "fundamentals"],
                        category="cv"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="High Volume Success Rate",
                        description="At least 80% of queries should succeed under high volume",
                        threshold=0.8,
                        metric="success_rate"
                    ),
                    ValidationCriterion(
                        name="Load Response Time",
                        description="Average response time should be under 5 seconds under load",
                        threshold=5.0,
                        metric="average_response_time"
                    )
                ],
                category="load_test"
            )
        ]

        return scenarios

    def get_edge_case_reliability_scenarios(self) -> List[TestScenario]:
        """Get edge case reliability test scenarios"""
        scenarios = [
            TestScenario(
                name="Long Query Test",
                description="Test reliability with very long queries",
                queries=[
                    TestQuery(
                        query_text="What are the detailed comparison between different humanoid robot locomotion techniques used in modern robotics research focusing on stability, energy efficiency, and adaptability to various terrains?",
                        expected_concepts=["humanoid", "locomotion", "stability", "energy efficiency", "terrains"],
                        category="edge_cases"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Long Query Handling",
                        description="System should handle long queries gracefully",
                        threshold=0.9,
                        metric="success_rate"
                    )
                ],
                category="edge_cases"
            ),
            TestScenario(
                name="Special Characters Test",
                description="Test reliability with queries containing special characters",
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
                category="edge_cases"
            )
        ]

        return scenarios

    def get_timeout_resilience_scenarios(self) -> List[TestScenario]:
        """Get scenarios for testing timeout resilience"""
        scenarios = [
            TestScenario(
                name="Timeout Recovery Test",
                description="Test that the system recovers gracefully from timeouts",
                queries=[
                    TestQuery(
                        query_text="Quantum computing applications",
                        expected_concepts=["quantum computing", "applications", "quantum"],
                        category="quantum"
                    ),
                    TestQuery(
                        query_text="Edge computing in robotics",
                        expected_concepts=["edge computing", "robotics", "IoT"],
                        category="edge_computing"
                    )
                ],
                success_criteria=[
                    ValidationCriterion(
                        name="Timeout Recovery Rate",
                        description="System should recover from timeouts and continue processing",
                        threshold=0.85,
                        metric="recovery_rate"
                    )
                ],
                category="resilience"
            )
        ]

        return scenarios

    def get_all_reliability_scenarios(self) -> List[TestScenario]:
        """Get all reliability test scenarios"""
        all_scenarios = []
        all_scenarios.extend(self.get_basic_reliability_scenarios())
        all_scenarios.extend(self.get_load_test_scenarios())
        all_scenarios.extend(self.get_edge_case_reliability_scenarios())
        all_scenarios.extend(self.get_timeout_resilience_scenarios())

        return all_scenarios