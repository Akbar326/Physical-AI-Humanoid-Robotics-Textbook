"""
Performance optimizer service based on validation results
"""

from typing import Dict, Any, List, Optional, Callable
import logging
import time
from dataclasses import dataclass
from enum import Enum


logger = logging.getLogger(__name__)


class OptimizationTarget(Enum):
    """Enumeration for optimization targets"""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    MEMORY_USAGE = "memory_usage"
    ACCURACY = "accuracy"
    RELIABILITY = "reliability"


class OptimizationStrategy(Enum):
    """Enumeration for optimization strategies"""
    CACHING = "caching"
    BATCHING = "batching"
    PARALLELIZATION = "parallelization"
    INDEXING = "indexing"
    ALGORITHM_TUNING = "algorithm_tuning"
    RESOURCE_SCALING = "resource_scaling"


@dataclass
class OptimizationRecommendation:
    """Data class for optimization recommendations"""
    strategy: OptimizationStrategy
    target: OptimizationTarget
    priority: int  # 1-5 scale, 5 being highest priority
    estimated_improvement: float  # Expected improvement percentage
    implementation_effort: int  # 1-5 scale, 5 being highest effort
    description: str
    implementation_notes: Optional[str] = None


class PerformanceOptimizer:
    """Service for optimizing performance based on validation results"""

    def __init__(self):
        self.optimization_history: List[Dict[str, Any]] = []
        self.current_config = {
            'cache_enabled': True,
            'batch_size': 10,
            'parallel_workers': 4,
            'timeout_threshold': 30.0,
            'relevance_threshold': 0.7
        }

    def analyze_validation_results(self, validation_results: List[Dict[str, Any]]) -> List[OptimizationRecommendation]:
        """
        Analyze validation results and generate optimization recommendations

        Args:
            validation_results: List of validation results to analyze

        Returns:
            List of optimization recommendations
        """
        recommendations = []

        if not validation_results:
            return recommendations

        # Calculate performance metrics
        response_times = [result.get('response_time', 0) for result in validation_results
                         if 'response_time' in result and result['response_time'] is not None]

        relevance_scores = [result.get('relevance_score', 0) for result in validation_results
                           if 'relevance_score' in result and result['relevance_score'] is not None]

        success_rate = sum(1 for result in validation_results if result.get('passed', False)) / len(validation_results) if validation_results else 0

        # Analyze response times
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)

            # If response times are too high, recommend caching
            if avg_response_time > 5.0:  # More than 5 seconds
                recommendations.append(
                    OptimizationRecommendation(
                        strategy=OptimizationStrategy.CACHING,
                        target=OptimizationTarget.RESPONSE_TIME,
                        priority=5,
                        estimated_improvement=60.0,
                        implementation_effort=3,
                        description="Implement query result caching to reduce response times",
                        implementation_notes="Cache frequently requested queries and their results"
                    )
                )

            # If response times are high, recommend batching
            elif avg_response_time > 2.0:
                recommendations.append(
                    OptimizationRecommendation(
                        strategy=OptimizationStrategy.BATCHING,
                        target=OptimizationTarget.RESPONSE_TIME,
                        priority=4,
                        estimated_improvement=30.0,
                        implementation_effort=4,
                        description="Implement batch processing for multiple queries",
                        implementation_notes="Group similar queries to reduce overhead"
                    )
                )

        # Analyze relevance scores
        if relevance_scores:
            avg_relevance_score = sum(relevance_scores) / len(relevance_scores)

            # If relevance scores are low, recommend algorithm tuning
            if avg_relevance_score < 0.7:
                recommendations.append(
                    OptimizationRecommendation(
                        strategy=OptimizationStrategy.ALGORITHM_TUNING,
                        target=OptimizationTarget.ACCURACY,
                        priority=5,
                        estimated_improvement=25.0,
                        implementation_effort=5,
                        description="Tune search algorithm parameters for better relevance",
                        implementation_notes="Adjust weighting of different relevance factors"
                    )
                )

        # Analyze success rate
        if success_rate < 0.9:
            recommendations.append(
                OptimizationRecommendation(
                    strategy=OptimizationStrategy.RESOURCE_SCALING,
                    target=OptimizationTarget.RELIABILITY,
                    priority=4,
                    estimated_improvement=15.0,
                    implementation_effort=4,
                    description="Scale resources to improve success rate",
                    implementation_notes="Increase timeout thresholds or add redundancy"
                )
            )

        # Sort recommendations by priority
        recommendations.sort(key=lambda x: x.priority, reverse=True)

        return recommendations

    def optimize_for_response_time(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate specific optimizations for response time improvement

        Args:
            validation_results: Validation results to analyze

        Returns:
            Dictionary with response time optimization recommendations
        """
        response_times = [result.get('response_time', 0) for result in validation_results
                         if 'response_time' in result and result['response_time'] is not None]

        if not response_times:
            return {'recommendations': [], 'current_avg_time': 0}

        current_avg_time = sum(response_times) / len(response_times)

        recommendations = [
            OptimizationRecommendation(
                strategy=OptimizationStrategy.CACHING,
                target=OptimizationTarget.RESPONSE_TIME,
                priority=5,
                estimated_improvement=50.0,
                implementation_effort=3,
                description="Implement result caching for frequent queries"
            ),
            OptimizationRecommendation(
                strategy=OptimizationStrategy.PARALLELIZATION,
                target=OptimizationTarget.RESPONSE_TIME,
                priority=4,
                estimated_improvement=30.0,
                implementation_effort=4,
                description="Process queries in parallel where possible"
            )
        ]

        return {
            'current_avg_time': current_avg_time,
            'recommendations': recommendations,
            'optimization_target': 'response_time'
        }

    def optimize_for_accuracy(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate specific optimizations for accuracy improvement

        Args:
            validation_results: Validation results to analyze

        Returns:
            Dictionary with accuracy optimization recommendations
        """
        relevance_scores = [result.get('relevance_score', 0) for result in validation_results
                           if 'relevance_score' in result and result['relevance_score'] is not None]

        if not relevance_scores:
            return {'recommendations': [], 'current_avg_relevance': 0}

        current_avg_relevance = sum(relevance_scores) / len(relevance_scores)

        recommendations = [
            OptimizationRecommendation(
                strategy=OptimizationStrategy.ALGORITHM_TUNING,
                target=OptimizationTarget.ACCURACY,
                priority=5,
                estimated_improvement=20.0,
                implementation_effort=5,
                description="Fine-tune relevance scoring algorithm"
            ),
            OptimizationRecommendation(
                strategy=OptimizationStrategy.INDEXING,
                target=OptimizationTarget.ACCURACY,
                priority=4,
                estimated_improvement=15.0,
                implementation_effort=4,
                description="Improve indexing strategy for better retrieval"
            )
        ]

        return {
            'current_avg_relevance': current_avg_relevance,
            'recommendations': recommendations,
            'optimization_target': 'accuracy'
        }

    def apply_optimization(self, strategy: OptimizationStrategy, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Apply a specific optimization strategy to the system

        Args:
            strategy: The strategy to apply
            validation_results: Current validation results

        Returns:
            Dictionary with optimization results
        """
        logger.info(f"Applying optimization strategy: {strategy.value}")

        optimization_result = {
            'strategy_applied': strategy.value,
            'timestamp': time.time(),
            'config_changes': {},
            'estimated_impact': {}
        }

        if strategy == OptimizationStrategy.CACHING:
            # Enable or enhance caching
            self.current_config['cache_enabled'] = True
            optimization_result['config_changes']['cache_enabled'] = True
            optimization_result['estimated_impact']['response_time_improvement'] = 0.5  # 50% improvement

        elif strategy == OptimizationStrategy.BATCHING:
            # Increase batch size
            self.current_config['batch_size'] = min(self.current_config['batch_size'] * 2, 50)
            optimization_result['config_changes']['batch_size'] = self.current_config['batch_size']
            optimization_result['estimated_impact']['throughput_improvement'] = 0.3  # 30% improvement

        elif strategy == OptimizationStrategy.PARALLELIZATION:
            # Increase parallel workers
            self.current_config['parallel_workers'] = min(self.current_config['parallel_workers'] + 2, 16)
            optimization_result['config_changes']['parallel_workers'] = self.current_config['parallel_workers']
            optimization_result['estimated_impact']['response_time_improvement'] = 0.4  # 40% improvement

        elif strategy == OptimizationStrategy.ALGORITHM_TUNING:
            # Adjust relevance threshold
            self.current_config['relevance_threshold'] = max(self.current_config['relevance_threshold'] - 0.1, 0.5)
            optimization_result['config_changes']['relevance_threshold'] = self.current_config['relevance_threshold']
            optimization_result['estimated_impact']['accuracy_improvement'] = 0.15  # 15% improvement

        elif strategy == OptimizationStrategy.RESOURCE_SCALING:
            # Increase timeout threshold
            self.current_config['timeout_threshold'] = self.current_config['timeout_threshold'] * 1.5
            optimization_result['config_changes']['timeout_threshold'] = self.current_config['timeout_threshold']
            optimization_result['estimated_impact']['success_rate_improvement'] = 0.1  # 10% improvement

        # Log the optimization
        self.optimization_history.append(optimization_result)

        return optimization_result

    def get_performance_trend_analysis(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze performance trends from validation results

        Args:
            validation_results: List of validation results with timestamps

        Returns:
            Dictionary with trend analysis
        """
        if not validation_results:
            return {'trends': {}, 'recommendations': []}

        # Group results by time period if timestamps are available
        response_times = []
        relevance_scores = []
        success_rates = []

        for result in validation_results:
            if 'response_time' in result:
                response_times.append(result['response_time'])
            if 'relevance_score' in result:
                relevance_scores.append(result['relevance_score'])
            if 'passed' in result:
                success_rates.append(1 if result['passed'] else 0)

        analysis = {
            'response_time_trend': self._analyze_trend(response_times),
            'relevance_trend': self._analyze_trend(relevance_scores),
            'success_rate_trend': self._analyze_trend(success_rates),
            'current_metrics': {
                'avg_response_time': sum(response_times) / len(response_times) if response_times else 0,
                'avg_relevance_score': sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0,
                'success_rate': sum(success_rates) / len(success_rates) if success_rates else 0
            }
        }

        # Generate recommendations based on trends
        recommendations = []
        if analysis['response_time_trend'] == 'degrading':
            recommendations.append(
                OptimizationRecommendation(
                    strategy=OptimizationStrategy.CACHING,
                    target=OptimizationTarget.RESPONSE_TIME,
                    priority=5,
                    estimated_improvement=50.0,
                    implementation_effort=3,
                    description="Response times are degrading, implement caching"
                )
            )

        if analysis['relevance_trend'] == 'degrading':
            recommendations.append(
                OptimizationRecommendation(
                    strategy=OptimizationStrategy.ALGORITHM_TUNING,
                    target=OptimizationTarget.ACCURACY,
                    priority=5,
                    estimated_improvement=20.0,
                    implementation_effort=5,
                    description="Relevance scores are degrading, tune algorithms"
                )
            )

        analysis['recommendations'] = recommendations
        return analysis

    def _analyze_trend(self, values: List[float]) -> str:
        """Analyze trend direction for a series of values"""
        if len(values) < 3:
            return 'insufficient_data'

        # Simple trend analysis: compare first and last values
        if len(values) >= 2:
            if values[-1] > values[0] * 1.1:  # 10% increase
                return 'degrading'
            elif values[-1] < values[0] * 0.9:  # 10% decrease
                return 'improving'
            else:
                return 'stable'

        return 'stable'

    def get_optimization_report(self, validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a comprehensive optimization report

        Args:
            validation_results: Validation results to analyze

        Returns:
            Dictionary with optimization report
        """
        all_recommendations = self.analyze_validation_results(validation_results)
        response_time_opt = self.optimize_for_response_time(validation_results)
        accuracy_opt = self.optimize_for_accuracy(validation_results)
        trend_analysis = self.get_performance_trend_analysis(validation_results)

        report = {
            'timestamp': time.time(),
            'total_validation_results': len(validation_results),
            'all_recommendations': [
                {
                    'strategy': rec.strategy.value,
                    'target': rec.target.value,
                    'priority': rec.priority,
                    'estimated_improvement': rec.estimated_improvement,
                    'implementation_effort': rec.implementation_effort,
                    'description': rec.description,
                    'implementation_notes': rec.implementation_notes
                }
                for rec in all_recommendations
            ],
            'response_time_optimizations': response_time_opt,
            'accuracy_optimizations': accuracy_opt,
            'trend_analysis': trend_analysis,
            'current_config': self.current_config.copy(),
            'optimization_history_count': len(self.optimization_history)
        }

        return report

    def auto_optimize(self, validation_results: List[Dict[str, Any]], max_recommendations: int = 3) -> List[Dict[str, Any]]:
        """
        Automatically apply optimizations based on validation results

        Args:
            validation_results: Validation results to analyze
            max_recommendations: Maximum number of optimizations to apply

        Returns:
            List of applied optimization results
        """
        recommendations = self.analyze_validation_results(validation_results)
        applied_optimizations = []

        for i, rec in enumerate(recommendations[:max_recommendations]):
            if rec.priority >= 4:  # Only apply high priority optimizations automatically
                result = self.apply_optimization(rec.strategy, validation_results)
                applied_optimizations.append(result)
                logger.info(f"Auto-applied optimization: {rec.strategy.value} - Priority: {rec.priority}")

        return applied_optimizations

    def reset_to_baseline_config(self):
        """Reset configuration to baseline values"""
        self.current_config = {
            'cache_enabled': True,
            'batch_size': 10,
            'parallel_workers': 4,
            'timeout_threshold': 30.0,
            'relevance_threshold': 0.7
        }
        logger.info("Configuration reset to baseline values")


# Global performance optimizer instance
global_performance_optimizer = PerformanceOptimizer()


def get_performance_optimizer() -> PerformanceOptimizer:
    """Get the global performance optimizer instance"""
    return global_performance_optimizer