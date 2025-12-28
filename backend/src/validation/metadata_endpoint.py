"""
Metadata validation endpoint
"""

from typing import Dict, Any
from flask import Blueprint, request, jsonify
from src.services.metadata_service import MetadataService
from src.services.search_service import SearchService


metadata_bp = Blueprint('metadata', __name__)
metadata_service = MetadataService()
search_service = SearchService()


@metadata_bp.route('/validate', methods=['POST'])
def validate_metadata():
    """Validate metadata for search results"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract search results from request
        search_results = data.get('search_results', [])

        if not search_results:
            return jsonify({'error': 'No search results provided for validation'}), 400

        # Validate metadata for the search results
        validation_results = metadata_service.validate_search_result_metadata(search_results)
        summary = metadata_service.get_metadata_summary(search_results)

        return jsonify({
            'success': True,
            'validation_results': validation_results,
            'summary': summary
        })

    except Exception as e:
        return jsonify({'error': f'Error validating metadata: {str(e)}'}), 500


@metadata_bp.route('/validate-search-results', methods=['POST'])
def validate_search_results_with_metadata():
    """Perform search and validate metadata in one call"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        query_text = data.get('query_text')
        if not query_text:
            return jsonify({'error': 'Query text is required'}), 400

        top_k = data.get('top_k', 5)

        # Perform search with metadata validation
        search_results = search_service.search_with_metadata_validation(query_text, top_k)

        return jsonify({
            'success': True,
            'search_results': search_results
        })

    except Exception as e:
        return jsonify({'error': f'Error validating search results: {str(e)}'}), 500


@metadata_bp.route('/validate-single-metadata', methods=['POST'])
def validate_single_metadata():
    """Validate a single metadata entry"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract metadata from request
        chunk_id = data.get('chunk_id')
        content = data.get('content', '')
        source_url = data.get('source_url', '')

        if not chunk_id:
            return jsonify({'error': 'chunk_id is required'}), 400

        # Validate the metadata
        result = metadata_service.validate_result_metadata(chunk_id, content, source_url)

        return jsonify({
            'success': True,
            'validation_result': result
        })

    except Exception as e:
        return jsonify({'error': f'Error validating single metadata: {str(e)}'}), 500


@metadata_bp.route('/extract-metadata', methods=['POST'])
def extract_metadata():
    """Extract metadata from content"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        content = data.get('content', '')
        source_url = data.get('source_url')

        if not content:
            return jsonify({'error': 'Content is required'}), 400

        # Extract metadata from content
        extracted_metadata = metadata_service.extract_metadata_from_content(content, source_url)

        return jsonify({
            'success': True,
            'extracted_metadata': extracted_metadata
        })

    except Exception as e:
        return jsonify({'error': f'Error extracting metadata: {str(e)}'}), 500


@metadata_bp.route('/validate-consistency', methods=['POST'])
def validate_metadata_consistency():
    """Validate consistency across multiple metadata entries"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        metadata_list = data.get('metadata_list', [])

        if not metadata_list:
            return jsonify({'error': 'No metadata list provided'}), 400

        # Validate consistency across metadata entries
        consistency_result = metadata_service.validate_metadata_consistency(metadata_list)

        return jsonify({
            'success': True,
            'consistency_result': consistency_result
        })

    except Exception as e:
        return jsonify({'error': f'Error validating metadata consistency: {str(e)}'}), 500