"""
Unit tests for metadata validation
"""

import unittest
from unittest.mock import Mock, patch
from src.services.metadata_service import MetadataService
from src.services.metadata_validator import MetadataValidator
from src.services.validation_service import ValidationResult


class TestMetadataService(unittest.TestCase):
    """Unit tests for MetadataService"""

    def setUp(self):
        """Set up test fixtures"""
        self.metadata_service = MetadataService()

    def test_extract_urls(self):
        """Test URL extraction from text"""
        text = "Visit https://example.com and http://test.org for more info"
        urls = self.metadata_service._extract_urls(text)

        self.assertEqual(len(urls), 2)
        self.assertIn("https://example.com", urls)
        self.assertIn("http://test.org", urls)

    def test_extract_urls_no_urls(self):
        """Test URL extraction from text with no URLs"""
        text = "This text contains no URLs"
        urls = self.metadata_service._extract_urls(text)

        self.assertEqual(len(urls), 0)

    def test_extract_emails(self):
        """Test email extraction from text"""
        text = "Contact us at test@example.com or support@test.org"
        emails = self.metadata_service._extract_emails(text)

        self.assertEqual(len(emails), 2)
        self.assertIn("test@example.com", emails)
        self.assertIn("support@test.org", emails)

    def test_extract_emails_no_emails(self):
        """Test email extraction from text with no emails"""
        text = "This text contains no emails"
        emails = self.metadata_service._extract_emails(text)

        self.assertEqual(len(emails), 0)

    def test_get_first_paragraph(self):
        """Test getting first paragraph from text"""
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        first_paragraph = self.metadata_service._get_first_paragraph(text)

        self.assertEqual(first_paragraph, "First paragraph.")

    def test_get_first_paragraph_empty(self):
        """Test getting first paragraph from empty text"""
        text = ""
        first_paragraph = self.metadata_service._get_first_paragraph(text)

        self.assertEqual(first_paragraph, "")

    def test_get_last_paragraph(self):
        """Test getting last paragraph from text"""
        text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        last_paragraph = self.metadata_service._get_last_paragraph(text)

        self.assertEqual(last_paragraph, "Third paragraph.")

    def test_get_last_paragraph_empty(self):
        """Test getting last paragraph from empty text"""
        text = ""
        last_paragraph = self.metadata_service._get_last_paragraph(text)

        self.assertEqual(last_paragraph, "")

    def test_extract_metadata_from_content(self):
        """Test extracting metadata from content"""
        content = "This is a sample content with a URL https://example.com and email test@example.com"
        source_url = "https://source.com"

        metadata = self.metadata_service.extract_metadata_from_content(content, source_url)

        self.assertEqual(metadata['content_length'], len(content))
        self.assertEqual(metadata['word_count'], 12)
        self.assertEqual(metadata['character_count'], len(content))
        self.assertEqual(metadata['source_url'], source_url)
        self.assertIn('https://example.com', metadata['contains_urls'])
        self.assertIn('test@example.com', metadata['contains_emails'])

    def test_validate_result_metadata(self):
        """Test validating metadata for a search result"""
        chunk_id = "test_chunk_1"
        content = "This is test content"
        source_url = "https://example.com"

        result = self.metadata_service.validate_result_metadata(chunk_id, content, source_url)

        self.assertIsInstance(result, dict)
        self.assertIn('completeness_validation', result)
        self.assertIn('accuracy_validation', result)
        self.assertIn('metadata', result)
        self.assertIn('overall_valid', result)
        self.assertTrue(result['overall_valid'])

    def test_validate_result_metadata_invalid(self):
        """Test validating metadata for an invalid search result"""
        chunk_id = ""  # Invalid chunk_id
        content = ""
        source_url = "invalid-url"  # Invalid URL format

        result = self.metadata_service.validate_result_metadata(chunk_id, content, source_url)

        self.assertIsInstance(result, dict)
        self.assertIn('overall_valid', result)
        self.assertFalse(result['overall_valid'])

    def test_validate_search_result_metadata(self):
        """Test validating metadata for multiple search results"""
        search_results = [
            {'chunk_id': 'chunk_1', 'content': 'content 1', 'source_url': 'https://example.com'},
            {'chunk_id': 'chunk_2', 'content': 'content 2', 'source_url': 'https://test.com'}
        ]

        validation_results = self.metadata_service.validate_search_result_metadata(search_results)

        self.assertIsInstance(validation_results, list)
        self.assertEqual(len(validation_results), 2)
        for result in validation_results:
            self.assertIn('overall_valid', result)

    def test_get_metadata_summary(self):
        """Test getting metadata summary for search results"""
        search_results = [
            {'chunk_id': 'chunk_1', 'content': 'content 1', 'source_url': 'https://example.com'},
            {'chunk_id': 'chunk_2', 'content': 'content 2', 'source_url': 'https://test.com'}
        ]

        summary = self.metadata_service.get_metadata_summary(search_results)

        self.assertIsInstance(summary, dict)
        self.assertIn('total_results', summary)
        self.assertIn('valid_results', summary)
        self.assertIn('invalid_results', summary)
        self.assertIn('metadata_accuracy', summary)
        self.assertEqual(summary['total_results'], 2)

    def test_get_metadata_summary_empty(self):
        """Test getting metadata summary for empty search results"""
        search_results = []

        summary = self.metadata_service.get_metadata_summary(search_results)

        self.assertIsInstance(summary, dict)
        self.assertEqual(summary['total_results'], 0)
        self.assertEqual(summary['valid_results'], 0)
        self.assertEqual(summary['invalid_results'], 0)
        self.assertEqual(summary['metadata_accuracy'], 0.0)

    def test_enrich_metadata(self):
        """Test enriching existing metadata"""
        base_metadata = {
            'chunk_id': 'test_chunk',
            'url': 'https://example.com',
            'content': 'This is sample content with https://test.com'
        }

        enriched = self.metadata_service.enrich_metadata(base_metadata)

        self.assertIn('content_length', enriched)
        self.assertIn('word_count', enriched)
        self.assertIn('metadata_complete', enriched)
        self.assertIn('metadata_completeness_details', enriched)
        self.assertIn('https://test.com', enriched['contains_urls'])

    def test_validate_metadata_consistency(self):
        """Test validating consistency across multiple metadata entries"""
        metadata_list = [
            {'field1': 'value1', 'field2': 'value2'},
            {'field1': 'value1', 'field2': 'value2'},
            {'field1': 'value1', 'field2': 'value2'}
        ]

        consistency_result = self.metadata_service.validate_metadata_consistency(metadata_list)

        self.assertIsInstance(consistency_result, dict)
        self.assertTrue(consistency_result['consistent'])
        self.assertEqual(consistency_result['message'], "All metadata is consistent")

    def test_validate_metadata_consistency_inconsistent(self):
        """Test validating consistency with inconsistent metadata entries"""
        metadata_list = [
            {'field1': 'value1', 'field2': 'value2'},
            {'field1': 'value1', 'field2': 'value2'},
            {'field1': 'value1'}  # Missing field2
        ]

        consistency_result = self.metadata_service.validate_metadata_consistency(metadata_list)

        self.assertIsInstance(consistency_result, dict)
        self.assertFalse(consistency_result['consistent'])
        self.assertIn('consistency_issues', consistency_result['details'])


class TestMetadataValidator(unittest.TestCase):
    """Unit tests for MetadataValidator"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = MetadataValidator()

    def test_validate_complete_metadata(self):
        """Test validating complete metadata"""
        metadata = {
            'url': 'https://example.com',
            'chunk_id': 'test_chunk_1',
            'content': 'This is test content'
        }

        result = self.validator.validate(metadata)

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Metadata validation passed")

    def test_validate_missing_fields(self):
        """Test validating metadata with missing fields"""
        metadata = {
            'url': 'https://example.com',
            # Missing chunk_id and content
        }

        result = self.validator.validate(metadata)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.success)
        self.assertIn("Missing required metadata fields", result.message)
        self.assertIn('chunk_id', result.details['missing_fields'])
        self.assertIn('content', result.details['missing_fields'])

    def test_validate_invalid_url(self):
        """Test validating metadata with invalid URL"""
        metadata = {
            'url': 'not-a-url',
            'chunk_id': 'test_chunk_1',
            'content': 'This is test content'
        }

        result = self.validator.validate(metadata)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.success)
        self.assertIn("Invalid URL format", result.message)

    def test_validate_invalid_chunk_id(self):
        """Test validating metadata with invalid chunk ID"""
        metadata = {
            'url': 'https://example.com',
            'chunk_id': '',  # Empty chunk ID
            'content': 'This is test content'
        }

        result = self.validator.validate(metadata)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.success)
        # When chunk_id is empty, it's considered a missing required field
        self.assertIn("Missing required metadata fields", result.message)
        self.assertIn("chunk_id", result.message)

    def test_validate_invalid_content(self):
        """Test validating metadata with invalid content"""
        metadata = {
            'url': 'https://example.com',
            'chunk_id': 'test_chunk_1',
            'content': ''  # Empty content
        }

        result = self.validator.validate(metadata)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.success)
        # When content is empty, it's considered a missing required field
        self.assertIn("Missing required metadata fields", result.message)
        self.assertIn("content", result.message)

    def test_validate_batch(self):
        """Test validating a batch of metadata entries"""
        metadata_list = [
            {
                'url': 'https://example.com',
                'chunk_id': 'test_chunk_1',
                'content': 'This is test content'
            },
            {
                'url': 'https://example.com',
                'chunk_id': 'test_chunk_2',
                'content': 'This is more test content'
            }
        ]

        results = self.validator.validate_batch(metadata_list)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIsInstance(result, ValidationResult)
            self.assertTrue(result.success)

    def test_validate_metadata_completeness(self):
        """Test validating metadata completeness"""
        metadata = {
            'url': 'https://example.com',
            'chunk_id': 'test_chunk_1',
            'content': 'This is test content',
            'source': 'web',
            'created_at': '2023-01-01'
        }

        result = self.validator.validate_metadata_completeness(metadata)

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.success)
        self.assertIn("All required metadata fields are present", result.message)

    def test_validate_metadata_completeness_missing_fields(self):
        """Test validating metadata completeness with missing fields"""
        required_fields = ['url', 'chunk_id', 'content', 'source', 'created_at']
        metadata = {
            'url': 'https://example.com',
            'chunk_id': 'test_chunk_1',
            # Missing content, source, and created_at
        }

        result = self.validator.validate_metadata_completeness(metadata, required_fields)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.success)
        self.assertIn("Missing required metadata fields", result.message)

    def test_validate_metadata_accuracy(self):
        """Test validating metadata accuracy"""
        metadata = {
            'url': 'https://example.com',
            'chunk_id': 'test_chunk_1',
            'content': 'This is test content'
        }
        expected_values = {
            'url': 'https://example.com',
            'chunk_id': 'test_chunk_1'
        }

        result = self.validator.validate_metadata_accuracy(metadata, expected_values)

        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.success)
        self.assertIn("Metadata accuracy validation passed", result.message)

    def test_validate_metadata_accuracy_inaccurate(self):
        """Test validating metadata accuracy with inaccurate values"""
        metadata = {
            'url': 'https://example.com',
            'chunk_id': 'test_chunk_1',
            'content': 'This is test content'
        }
        expected_values = {
            'url': 'https://different.com',  # Different URL
            'chunk_id': 'test_chunk_1'
        }

        result = self.validator.validate_metadata_accuracy(metadata, expected_values)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.success)
        self.assertIn("Metadata accuracy validation failed", result.message)
        self.assertIn('url', [f['field'] for f in result.details['inaccurate_fields']])

    def test_validate_url_accessibility(self):
        """Test validating URL accessibility"""
        # This test will mock the requests.head call since we don't want to make actual HTTP requests
        with patch('requests.head') as mock_head:
            mock_head.return_value.status_code = 200

            result = self.validator.validate_url_accessibility('https://example.com')

            self.assertIsInstance(result, ValidationResult)
            self.assertTrue(result.success)
            self.assertIn("URL accessibility: ✓", result.message)
            self.assertEqual(result.details['status_code'], 200)

    def test_validate_url_accessibility_unreachable(self):
        """Test validating URL accessibility for unreachable URL"""
        # This test will mock the requests.head call since we don't want to make actual HTTP requests
        with patch('requests.head') as mock_head:
            mock_head.return_value.status_code = 404

            result = self.validator.validate_url_accessibility('https://example.com')

            self.assertIsInstance(result, ValidationResult)
            self.assertFalse(result.success)
            self.assertIn("URL accessibility: ✗", result.message)
            self.assertEqual(result.details['status_code'], 404)


if __name__ == '__main__':
    unittest.main()