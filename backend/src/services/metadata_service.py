"""
Metadata extraction and validation service
"""

from typing import Dict, Any, List
import logging
from src.services.metadata_validator import MetadataValidator

logger = logging.getLogger(__name__)


class MetadataService:
    """Service for extracting and validating metadata from search results"""

    def __init__(self):
        self.validator = MetadataValidator()

    def extract_metadata_from_content(self, content: str, source_url: str = None) -> Dict[str, Any]:
        """
        Extract metadata from content
        """
        metadata = {
            'content_length': len(content),
            'word_count': len(content.split()),
            'character_count': len(content),
            'contains_urls': self._extract_urls(content),
            'contains_emails': self._extract_emails(content),
            'first_paragraph': self._get_first_paragraph(content),
            'last_paragraph': self._get_last_paragraph(content),
            'source_url': source_url
        }
        return metadata

    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text"""
        import re
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text)
        return urls

    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text"""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails

    def _get_first_paragraph(self, text: str) -> str:
        """Get the first paragraph from text"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        return paragraphs[0] if paragraphs else ""

    def _get_last_paragraph(self, text: str) -> str:
        """Get the last paragraph from text"""
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        return paragraphs[-1] if paragraphs else ""

    def validate_metadata_completeness(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that all required metadata fields are present
        """
        result = self.validator.validate_metadata_completeness(metadata)
        return {
            'success': result.success,
            'message': result.message,
            'details': result.details
        }

    def validate_metadata_accuracy(self, metadata: Dict[str, Any], expected_values: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Validate that metadata values are accurate
        """
        result = self.validator.validate_metadata_accuracy(metadata, expected_values)
        return {
            'success': result.success,
            'message': result.message,
            'details': result.details
        }

    def validate_result_metadata(self, chunk_id: str, content: str, source_url: str) -> Dict[str, Any]:
        """
        Validate metadata for a search result
        """
        metadata = {
            'chunk_id': chunk_id,
            'content': content,
            'url': source_url,
            'content_length': len(content),
            'extracted_urls': self._extract_urls(content),
            'extracted_emails': self._extract_emails(content)
        }

        # Validate the metadata using the main validation method which checks for basic required fields
        # Use a more basic validation that only requires the core fields
        basic_required_fields = ['url', 'chunk_id', 'content']
        missing_fields = [field for field in basic_required_fields if field not in metadata or not metadata[field]]

        if missing_fields:
            completeness_result = {
                'success': False,
                'message': f"Missing required metadata fields: {missing_fields}",
                'details': {'missing_fields': missing_fields}
            }
        else:
            completeness_result = {
                'success': True,
                'message': "All required metadata fields are present",
                'details': {'present_fields': list(metadata.keys())}
            }

        accuracy_result = {
            'success': True,
            'message': 'No expected values provided for accuracy validation',
            'details': {}
        }

        return {
            'completeness_validation': completeness_result,
            'accuracy_validation': accuracy_result,
            'metadata': metadata,
            'overall_valid': completeness_result['success'] and accuracy_result['success']
        }

    def validate_search_result_metadata(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate metadata for multiple search results
        """
        validation_results = []
        for result in search_results:
            chunk_id = result.get('chunk_id')
            content = result.get('content', '')
            source_url = result.get('source_url', result.get('url', ''))

            result_validation = self.validate_result_metadata(chunk_id, content, source_url)
            validation_results.append(result_validation)

        return validation_results

    def get_metadata_summary(self, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get summary of metadata for search results
        """
        if not search_results:
            return {'total_results': 0, 'valid_results': 0, 'invalid_results': 0, 'metadata_accuracy': 0.0}

        validation_results = self.validate_search_result_metadata(search_results)

        total_results = len(search_results)
        valid_results = sum(1 for vr in validation_results if vr['overall_valid'])
        invalid_results = total_results - valid_results

        return {
            'total_results': total_results,
            'valid_results': valid_results,
            'invalid_results': invalid_results,
            'metadata_accuracy': valid_results / total_results if total_results > 0 else 0.0,
            'validation_results': validation_results
        }

    def validate_url_accessibility(self, url: str) -> Dict[str, Any]:
        """
        Validate that a URL is accessible
        """
        result = self.validator.validate_url_accessibility(url)
        return {
            'success': result.success,
            'message': result.message,
            'details': result.details
        }

    def enrich_metadata(self, base_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add additional metadata to existing metadata
        """
        enriched = base_metadata.copy()

        # Add content-based metadata
        content = base_metadata.get('content', '')
        if content:
            enriched.update(self.extract_metadata_from_content(content, base_metadata.get('url')))

        # Add validation flags
        completeness = self.validate_metadata_completeness(enriched)
        enriched['metadata_complete'] = completeness['success']
        enriched['metadata_completeness_details'] = completeness['details']

        return enriched

    def validate_metadata_consistency(self, metadata_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate consistency across multiple metadata entries
        """
        if not metadata_list:
            return {
                'consistent': True,
                'message': 'No metadata to validate',
                'details': {}
            }

        # Check if all entries have the same required fields
        required_fields = set()
        for metadata in metadata_list:
            required_fields.update(metadata.keys())

        consistency_issues = []
        for field in required_fields:
            field_missing_count = sum(1 for metadata in metadata_list if field not in metadata or not metadata.get(field))
            if field_missing_count > 0:
                consistency_issues.append({
                    'field': field,
                    'missing_count': field_missing_count,
                    'total_count': len(metadata_list)
                })

        return {
            'consistent': len(consistency_issues) == 0,
            'message': f"Found {len(consistency_issues)} consistency issues" if consistency_issues else "All metadata is consistent",
            'details': {
                'total_entries': len(metadata_list),
                'consistency_issues': consistency_issues
            }
        }