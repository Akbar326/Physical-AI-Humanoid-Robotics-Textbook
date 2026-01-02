"""
Base Validation Service for the RAG pipeline validation system
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of a validation operation"""
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None
    execution_time: Optional[float] = None


class ValidationService(ABC):
    """Base class for all validation services"""

    def __init__(self):
        self.name = self.__class__.__name__

    def validate_with_timing(self, *args, **kwargs) -> ValidationResult:
        """Execute validation with timing information"""
        start_time = time.time()
        try:
            result = self.validate(*args, **kwargs)
            execution_time = time.time() - start_time
            result.execution_time = execution_time
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Validation failed: {str(e)}", exc_info=True)
            return ValidationResult(
                success=False,
                message=f"Validation failed: {str(e)}",
                execution_time=execution_time
            )

    @abstractmethod
    def validate(self, *args, **kwargs) -> ValidationResult:
        """Execute the validation logic - to be implemented by subclasses"""
        pass

    def validate_batch(self, items: List[Any]) -> List[ValidationResult]:
        """Validate a batch of items"""
        results = []
        for item in items:
            result = self.validate(item)
            results.append(result)
        return results

    def get_validation_stats(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Calculate statistics for a batch of validation results"""
        total = len(results)
        successful = sum(1 for r in results if r.success)
        failed = total - successful
        success_rate = successful / total if total > 0 else 0

        avg_execution_time = sum(r.execution_time or 0 for r in results) / total if total > 0 else 0

        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': success_rate,
            'average_execution_time': avg_execution_time
        }

    def validate_metadata_accuracy(self, actual_metadata: Dict[str, Any], expected_metadata: Dict[str, Any] = None) -> ValidationResult:
        """Validate that metadata values are accurate by comparing to expected values"""
        if expected_metadata is None:
            # If no expected values provided, just validate that required fields exist
            required_fields = ['url', 'chunk_id', 'content']
            missing_fields = [field for field in required_fields if field not in actual_metadata or not actual_metadata[field]]

            if missing_fields:
                return ValidationResult(
                    success=False,
                    message=f"Missing required metadata fields: {missing_fields}",
                    details={'missing_fields': missing_fields}
                )

            return ValidationResult(
                success=True,
                message="Metadata contains all required fields",
                details={'present_fields': list(actual_metadata.keys())}
            )

        # Compare actual metadata with expected values
        inaccurate_fields = []
        for field, expected_value in expected_metadata.items():
            actual_value = actual_metadata.get(field)
            if actual_value != expected_value:
                inaccurate_fields.append({
                    'field': field,
                    'expected': expected_value,
                    'actual': actual_value
                })

        if inaccurate_fields:
            return ValidationResult(
                success=False,
                message=f"Metadata accuracy validation failed for fields: {[f['field'] for f in inaccurate_fields]}",
                details={'inaccurate_fields': inaccurate_fields}
            )

        return ValidationResult(
            success=True,
            message="Metadata accuracy validation passed",
            details={'validated_fields': list(expected_metadata.keys())}
        )