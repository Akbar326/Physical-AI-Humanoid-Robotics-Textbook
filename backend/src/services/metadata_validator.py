"""
Metadata validation service
"""

from typing import Dict, Any, List
import logging
from src.services.validation_service import ValidationService, ValidationResult

logger = logging.getLogger(__name__)


class MetadataValidator(ValidationService):
    """Validator for metadata accuracy and completeness"""

    def __init__(self):
        super().__init__()

    def validate(self, metadata: Dict[str, Any]) -> ValidationResult:
        """
        Validate metadata for accuracy and completeness
        """
        try:
            # Check required fields
            required_fields = ['url', 'chunk_id', 'content']
            missing_fields = [field for field in required_fields if field not in metadata or not metadata[field]]

            if missing_fields:
                return ValidationResult(
                    success=False,
                    message=f"Missing required metadata fields: {missing_fields}",
                    details={'missing_fields': missing_fields, 'provided_metadata': list(metadata.keys())}
                )

            # Validate URL format
            url = metadata.get('url', '')
            if not self._is_valid_url(url):
                return ValidationResult(
                    success=False,
                    message=f"Invalid URL format: {url}",
                    details={'url': url, 'field': 'url'}
                )

            # Validate chunk_id
            chunk_id = metadata.get('chunk_id', '')
            if not self._is_valid_chunk_id(chunk_id):
                return ValidationResult(
                    success=False,
                    message=f"Invalid chunk ID: {chunk_id}",
                    details={'chunk_id': chunk_id, 'field': 'chunk_id'}
                )

            # Validate content
            content = metadata.get('content', '')
            if not self._is_valid_content(content):
                return ValidationResult(
                    success=False,
                    message="Content is empty or invalid",
                    details={'content_length': len(content), 'field': 'content'}
                )

            # All validations passed
            return ValidationResult(
                success=True,
                message="Metadata validation passed",
                details={
                    'url': url,
                    'chunk_id': chunk_id,
                    'content_length': len(content),
                    'additional_metadata_keys': [k for k in metadata.keys() if k not in required_fields]
                }
            )
        except Exception as e:
            logger.error(f"Error validating metadata: {str(e)}", exc_info=True)
            return ValidationResult(
                success=False,
                message=f"Error during metadata validation: {str(e)}",
                details={'error': str(e)}
            )

    def validate_batch(self, metadata_list: List[Dict[str, Any]]) -> List[ValidationResult]:
        """
        Validate a batch of metadata entries
        """
        results = []
        for metadata in metadata_list:
            result = self.validate(metadata)
            results.append(result)
        return results

    def validate_metadata_completeness(self, metadata: Dict[str, Any], required_fields: List[str] = None) -> ValidationResult:
        """
        Validate that all required metadata fields are present
        """
        if required_fields is None:
            required_fields = ['url', 'chunk_id', 'content', 'source', 'created_at']

        missing_fields = []
        for field in required_fields:
            if field not in metadata or metadata[field] is None or (isinstance(metadata[field], str) and not metadata[field].strip()):
                missing_fields.append(field)

        if missing_fields:
            return ValidationResult(
                success=False,
                message=f"Missing required metadata fields: {missing_fields}",
                details={'missing_fields': missing_fields, 'required_fields': required_fields}
            )

        return ValidationResult(
            success=True,
            message="All required metadata fields are present",
            details={'present_fields': [f for f in required_fields if f in metadata]}
        )

    def validate_metadata_accuracy(self, metadata: Dict[str, Any], expected_values: Dict[str, Any] = None) -> ValidationResult:
        """
        Validate that metadata values are accurate
        """
        if expected_values is None:
            expected_values = {}

        inaccurate_fields = []
        for field, expected_value in expected_values.items():
            actual_value = metadata.get(field)
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
            details={'validated_fields': list(expected_values.keys())}
        )

    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid"""
        if not url or not isinstance(url, str):
            return False
        # Basic URL validation: should start with http:// or https://
        return url.startswith(('http://', 'https://'))

    def _is_valid_chunk_id(self, chunk_id: str) -> bool:
        """Check if chunk ID is valid"""
        if not chunk_id or not isinstance(chunk_id, str):
            return False
        # Basic validation: non-empty string
        return len(chunk_id.strip()) > 0

    def _is_valid_content(self, content: str) -> bool:
        """Check if content is valid"""
        if content is None or not isinstance(content, str):
            return False
        # Basic validation: non-empty string
        return len(content.strip()) > 0

    def validate_url_accessibility(self, url: str) -> ValidationResult:
        """Validate that the URL is accessible"""
        import requests
        try:
            response = requests.head(url, timeout=10)
            is_accessible = response.status_code == 200
            return ValidationResult(
                success=is_accessible,
                message=f"URL accessibility: {'✓' if is_accessible else '✗'}",
                details={
                    'url': url,
                    'status_code': response.status_code,
                    'accessible': is_accessible
                }
            )
        except Exception as e:
            return ValidationResult(
                success=False,
                message=f"Error checking URL accessibility: {str(e)}",
                details={
                    'url': url,
                    'error': str(e)
                }
            )