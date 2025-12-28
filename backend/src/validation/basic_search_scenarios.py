"""
Basic test scenarios for semantic search validation
"""

from typing import List
from src.models.validation import TestQuery


class BasicSearchScenarios:
    """Collection of basic test scenarios for semantic search validation"""

    @staticmethod
    def get_ai_robotics_scenarios() -> List[TestQuery]:
        """Get test scenarios related to AI robotics"""
        return [
            TestQuery(
                query_text="AI robotics fundamentals",
                expected_concepts=["artificial intelligence", "robotics", "machine learning", "autonomous"],
                category="ai_robotics"
            ),
            TestQuery(
                query_text="robot learning algorithms",
                expected_concepts=["machine learning", "reinforcement learning", "neural networks", "training"],
                category="ai_robotics"
            ),
            TestQuery(
                query_text="computer vision in robotics",
                expected_concepts=["computer vision", "image processing", "object detection", "perception"],
                category="ai_robotics"
            )
        ]

    @staticmethod
    def get_humanoid_movement_scenarios() -> List[TestQuery]:
        """Get test scenarios related to humanoid movement"""
        return [
            TestQuery(
                query_text="humanoid movement principles",
                expected_concepts=["locomotion", "bipedal", "motion planning", "kinematics"],
                category="humanoid_movement"
            ),
            TestQuery(
                query_text="balance control in robots",
                expected_concepts=["balance", "stability", "control systems", "posture"],
                category="humanoid_movement"
            ),
            TestQuery(
                query_text="motion planning for bipedal robots",
                expected_concepts=["motion planning", "path planning", "trajectory", "walking"],
                category="humanoid_movement"
            )
        ]

    @staticmethod
    def get_physical_ai_scenarios() -> List[TestQuery]:
        """Get test scenarios related to physical AI"""
        return [
            TestQuery(
                query_text="physical AI concepts",
                expected_concepts=["embodied AI", "physical interaction", "robotics", "real-world"],
                category="physical_ai"
            ),
            TestQuery(
                query_text="embodied intelligence",
                expected_concepts=["embodied", "cognition", "physical", "environment interaction"],
                category="physical_ai"
            ),
            TestQuery(
                query_text="real-world AI applications",
                expected_concepts=["real-world", "applications", "physical", "deployment"],
                category="physical_ai"
            )
        ]

    @staticmethod
    def get_basic_semantic_search_scenarios() -> List[TestQuery]:
        """Get comprehensive set of basic semantic search test scenarios"""
        scenarios = []
        scenarios.extend(BasicSearchScenarios.get_ai_robotics_scenarios())
        scenarios.extend(BasicSearchScenarios.get_humanoid_movement_scenarios())
        scenarios.extend(BasicSearchScenarios.get_physical_ai_scenarios())
        return scenarios

    @staticmethod
    def get_edge_case_scenarios() -> List[TestQuery]:
        """Get edge case test scenarios"""
        return [
            TestQuery(
                query_text="AI",  # Very short query
                expected_concepts=["artificial intelligence", "AI", "machine learning"],
                category="edge_cases"
            ),
            TestQuery(
                query_text="robot",  # Single word query
                expected_concepts=["robot", "robotics", "automation"],
                category="edge_cases"
            ),
            TestQuery(
                query_text="What is machine learning?",  # Question format
                expected_concepts=["machine learning", "ML", "algorithms", "learning"],
                category="edge_cases"
            )
        ]

    @staticmethod
    def get_performance_test_scenarios() -> List[TestQuery]:
        """Get scenarios for performance testing"""
        return [
            TestQuery(
                query_text="performance of AI systems",
                expected_concepts=["performance", "efficiency", "optimization", "speed"],
                category="performance"
            ),
            TestQuery(
                query_text="computational efficiency in robotics",
                expected_concepts=["efficiency", "computation", "optimization", "resources"],
                category="performance"
            )
        ]

    @staticmethod
    def get_all_scenarios() -> List[TestQuery]:
        """Get all available test scenarios"""
        all_scenarios = []
        all_scenarios.extend(BasicSearchScenarios.get_ai_robotics_scenarios())
        all_scenarios.extend(BasicSearchScenarios.get_humanoid_movement_scenarios())
        all_scenarios.extend(BasicSearchScenarios.get_physical_ai_scenarios())
        all_scenarios.extend(BasicSearchScenarios.get_edge_case_scenarios())
        all_scenarios.extend(BasicSearchScenarios.get_performance_test_scenarios())
        return all_scenarios

    @staticmethod
    def get_mixed_complexity_scenarios() -> List[TestQuery]:
        """Get scenarios of varying complexity levels"""
        return [
            # Simple queries
            TestQuery(
                query_text="robot",
                expected_concepts=["robot", "robotics"],
                category="simple"
            ),
            # Medium complexity
            TestQuery(
                query_text="autonomous humanoid robot navigation",
                expected_concepts=["autonomous", "humanoid", "robot", "navigation", "path planning"],
                category="medium"
            ),
            # Complex queries
            TestQuery(
                query_text="challenges in developing efficient bipedal locomotion algorithms for humanoid robots in dynamic environments",
                expected_concepts=["bipedal", "locomotion", "algorithms", "humanoid", "dynamic environments", "challenges"],
                category="complex"
            )
        ]