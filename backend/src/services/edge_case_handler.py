"""
Edge case handling service for queries
"""

from typing import Dict, Any, Optional
import logging
import re
from urllib.parse import urlparse


logger = logging.getLogger(__name__)


class EdgeCaseHandler:
    """Service for handling edge cases in query processing"""

    def __init__(self):
        self.empty_query_threshold = 3  # Minimum length for a query to be considered non-empty
        self.long_query_threshold = 500  # Maximum length for a query before special handling
        self.special_char_patterns = [
            r'[<>"\'%;)',
            r'(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|SCRIPT)',
            r'(\.\./)',  # Path traversal
        ]

    def handle_query(self, query_text: str) -> Dict[str, Any]:
        """
        Handle a query and apply edge case processing as needed

        Args:
            query_text: The query text to process

        Returns:
            Dictionary with processed query and handling information
        """
        result = {
            'original_query': query_text,
            'processed_query': query_text,
            'is_valid': True,
            'is_safe': True,
            'edge_case_detected': False,
            'handling_applied': [],
            'warnings': []
        }

        # Check for empty or minimal queries
        if self._is_empty_query(query_text):
            result.update(self._handle_empty_query(query_text))
            result['edge_case_detected'] = True
            result['handling_applied'].append('empty_query_handling')

        # Check for very long queries
        if self._is_long_query(query_text):
            result.update(self._handle_long_query(query_text))
            result['edge_case_detected'] = True
            result['handling_applied'].append('long_query_handling')

        # Check for special characters that might indicate injection attempts
        unsafe_patterns = self._check_for_unsafe_patterns(query_text)
        if unsafe_patterns:
            result.update(self._handle_unsafe_query(query_text, unsafe_patterns))
            result['edge_case_detected'] = True
            result['handling_applied'].append('unsafe_query_handling')

        # Sanitize the query
        sanitized_query = self._sanitize_query(result['processed_query'])
        if sanitized_query != result['processed_query']:
            result['processed_query'] = sanitized_query
            result['handling_applied'].append('query_sanitization')

        # Normalize the query
        normalized_query = self._normalize_query(result['processed_query'])
        if normalized_query != result['processed_query']:
            result['processed_query'] = normalized_query
            result['handling_applied'].append('query_normalization')

        return result

    def _is_empty_query(self, query_text: str) -> bool:
        """Check if a query is empty or contains only whitespace"""
        return not query_text or len(query_text.strip()) < self.empty_query_threshold

    def _is_long_query(self, query_text: str) -> bool:
        """Check if a query is very long"""
        return len(query_text) > self.long_query_threshold

    def _check_for_unsafe_patterns(self, query_text: str) -> list:
        """Check for potentially unsafe patterns in the query"""
        unsafe_patterns = []
        query_lower = query_text.lower()

        for pattern in self.special_char_patterns:
            if re.search(pattern, query_text, re.IGNORECASE):
                unsafe_patterns.append(pattern)

        return unsafe_patterns

    def _handle_empty_query(self, query_text: str) -> Dict[str, Any]:
        """Handle empty or minimal queries"""
        logger.warning(f"Empty or minimal query detected: '{query_text}'")
        return {
            'processed_query': query_text.strip(),
            'is_valid': False,
            'warnings': ['Query is empty or too short']
        }

    def _handle_long_query(self, query_text: str) -> Dict[str, Any]:
        """Handle very long queries"""
        logger.warning(f"Very long query detected: {len(query_text)} characters")
        # Truncate to a reasonable length
        processed = query_text[:self.long_query_threshold]
        return {
            'processed_query': processed,
            'warnings': [f'Query was truncated from {len(query_text)} to {len(processed)} characters']
        }

    def _handle_unsafe_query(self, query_text: str, unsafe_patterns: list) -> Dict[str, Any]:
        """Handle potentially unsafe queries"""
        logger.warning(f"Potentially unsafe patterns detected in query: {unsafe_patterns}")
        return {
            'is_safe': False,
            'warnings': [f'Potentially unsafe patterns detected: {unsafe_patterns}']
        }

    def _sanitize_query(self, query_text: str) -> str:
        """Sanitize the query by removing potentially dangerous characters"""
        # Remove potential SQL injection patterns (basic approach)
        sanitized = re.sub(r'[<>"\']', '', query_text)
        return sanitized

    def _normalize_query(self, query_text: str) -> str:
        """Normalize the query by standardizing whitespace and case where appropriate"""
        # Normalize whitespace
        normalized = re.sub(r'\s+', ' ', query_text.strip())
        return normalized

    def validate_url_safety(self, url: str) -> Dict[str, Any]:
        """
        Validate the safety of a URL

        Args:
            url: URL to validate

        Returns:
            Dictionary with validation results
        """
        result = {
            'url': url,
            'is_valid': True,
            'is_safe': True,
            'issues': []
        }

        try:
            parsed = urlparse(url)

            # Check if URL is valid
            if not parsed.scheme or not parsed.netloc:
                result['is_valid'] = False
                result['issues'].append('Invalid URL format')
                return result

            # Check for suspicious schemes
            if parsed.scheme.lower() not in ['http', 'https']:
                result['is_safe'] = False
                result['issues'].append(f'Unsafe scheme: {parsed.scheme}')

            # Check for path traversal
            if '..' in parsed.path:
                result['is_safe'] = False
                result['issues'].append('Path traversal detected')

        except Exception as e:
            result['is_valid'] = False
            result['issues'].append(f'URL parsing error: {str(e)}')

        return result

    def handle_content(self, content: str) -> Dict[str, Any]:
        """
        Handle content and apply edge case processing

        Args:
            content: Content to process

        Returns:
            Dictionary with processed content and handling information
        """
        result = {
            'original_content': content,
            'processed_content': content,
            'is_valid': True,
            'is_safe': True,
            'edge_case_detected': False,
            'handling_applied': [],
            'warnings': []
        }

        # Check for very large content
        if len(content) > 10000:  # 10KB threshold
            result['processed_content'] = content[:10000]
            result['edge_case_detected'] = True
            result['handling_applied'].append('content_truncation')
            result['warnings'].append(f'Content was truncated from {len(content)} to 10000 characters')

        # Check for embedded URLs or scripts
        if self._contains_dangerous_content(content):
            result['is_safe'] = False
            result['warnings'].append('Potentially dangerous content detected')

        # Sanitize content
        sanitized_content = self._sanitize_content(result['processed_content'])
        if sanitized_content != result['processed_content']:
            result['processed_content'] = sanitized_content
            result['handling_applied'].append('content_sanitization')

        return result

    def _contains_dangerous_content(self, content: str) -> bool:
        """Check if content contains potentially dangerous elements"""
        dangerous_patterns = [
            r'<script',
            r'javascript:',
            r'vbscript:',
            r'on\w+\s*=',
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True

        return False

    def _sanitize_content(self, content: str) -> str:
        """Sanitize content by removing potentially dangerous elements"""
        # Remove script tags
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
        # Remove event handlers
        sanitized = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', '', sanitized, flags=re.IGNORECASE)
        return sanitized

    def detect_and_handle_encoding_issues(self, text: str) -> Dict[str, Any]:
        """
        Detect and handle text encoding issues

        Args:
            text: Text to check for encoding issues

        Returns:
            Dictionary with encoding handling results
        """
        result = {
            'original_text': text,
            'processed_text': text,
            'encoding_issues_detected': False,
            'encoding_issues_fixed': False,
            'warnings': []
        }

        try:
            # Try to encode/decode to detect encoding issues
            encoded = text.encode('utf-8')
            decoded = encoded.decode('utf-8')

            if decoded != text:
                result['encoding_issues_detected'] = True
                result['processed_text'] = decoded
                result['encoding_issues_fixed'] = True
                result['warnings'].append('Encoding issues detected and fixed')

        except UnicodeError as e:
            result['encoding_issues_detected'] = True
            result['is_valid'] = False
            result['warnings'].append(f'Unicode encoding error: {str(e)}')

            # Try to fix by encoding with error handling
            try:
                fixed_text = text.encode('utf-8', errors='replace').decode('utf-8')
                result['processed_text'] = fixed_text
                result['encoding_issues_fixed'] = True
            except Exception:
                result['processed_text'] = ""

        return result

    def validate_and_clean_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean metadata to handle edge cases

        Args:
            metadata: Metadata dictionary to validate and clean

        Returns:
            Dictionary with cleaned metadata and validation results
        """
        cleaned_metadata = metadata.copy()
        validation_result = {
            'original_metadata': metadata,
            'cleaned_metadata': cleaned_metadata,
            'validation_passed': True,
            'issues_found': [],
            'cleaned_fields': []
        }

        # Validate and clean URL fields
        for field_name in ['url', 'source_url', 'link']:
            if field_name in cleaned_metadata:
                url_result = self.validate_url_safety(cleaned_metadata[field_name])
                if not url_result['is_safe']:
                    validation_result['issues_found'].append(f"Unsafe URL in {field_name}: {url_result['issues']}")
                    # Optionally remove unsafe URLs
                    del cleaned_metadata[field_name]
                    validation_result['cleaned_fields'].append(field_name)

        # Check for oversized text fields
        for field_name, value in cleaned_metadata.items():
            if isinstance(value, str) and len(value) > 5000:  # 5KB threshold
                cleaned_metadata[field_name] = value[:5000]
                validation_result['cleaned_fields'].append(field_name)
                validation_result['issues_found'].append(f"Field {field_name} was truncated")

        validation_result['cleaned_metadata'] = cleaned_metadata
        validation_result['validation_passed'] = len(validation_result['issues_found']) == 0

        return validation_result