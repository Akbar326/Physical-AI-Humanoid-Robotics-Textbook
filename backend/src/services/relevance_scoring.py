"""
Relevance scoring logic service
"""

from typing import List, Dict, Any
import logging
import re
from collections import Counter

logger = logging.getLogger(__name__)


class RelevanceScoringService:
    """Service for calculating relevance scores between queries and content"""

    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }

    def calculate_relevance_score(self, query: str, content: str) -> float:
        """
        Calculate relevance score between query and content using multiple factors
        """
        if not query or not content:
            return 0.0

        # Normalize text
        query_normalized = self._normalize_text(query)
        content_normalized = self._normalize_text(content)

        # Calculate different relevance factors
        keyword_match_score = self._calculate_keyword_match_score(query_normalized, content_normalized)
        semantic_similarity_score = self._calculate_semantic_similarity_score(query_normalized, content_normalized)
        position_score = self._calculate_position_score(query_normalized, content_normalized)
        density_score = self._calculate_density_score(query_normalized, content_normalized)

        # Weighted combination of factors (weights sum to 1.0)
        final_score = (
            0.3 * keyword_match_score +
            0.4 * semantic_similarity_score +
            0.2 * position_score +
            0.1 * density_score
        )

        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, final_score))

    def _normalize_text(self, text: str) -> str:
        """Normalize text by converting to lowercase and removing extra whitespace"""
        return re.sub(r'\s+', ' ', text.lower().strip())

    def _calculate_keyword_match_score(self, query: str, content: str) -> float:
        """Calculate score based on keyword matches"""
        query_words = set(self._get_content_words(query))
        content_words = set(self._get_content_words(content))

        if not query_words:
            return 0.0

        matching_words = query_words.intersection(content_words)
        match_ratio = len(matching_words) / len(query_words)

        return min(1.0, match_ratio)  # Cap at 1.0

    def _calculate_semantic_similarity_score(self, query: str, content: str) -> float:
        """Calculate score based on semantic similarity using word overlap and context"""
        query_words = self._get_content_words(query)
        content_words = self._get_content_words(content)

        if not query_words:
            return 0.0

        # Count word occurrences
        query_word_counts = Counter(query_words)
        content_word_counts = Counter(content_words)

        # Calculate overlap with frequency consideration
        common_words_score = 0
        total_query_words = len(query_words)

        for word, query_count in query_word_counts.items():
            content_count = content_word_counts.get(word, 0)
            if content_count > 0:
                # Weight by minimum occurrence to handle phrases
                common_words_score += min(query_count, content_count)

        # Normalize by total query words
        semantic_score = common_words_score / total_query_words if total_query_words > 0 else 0

        return min(1.0, semantic_score)

    def _calculate_position_score(self, query: str, content: str) -> float:
        """Calculate score based on position of matching words in content"""
        query_words = self._get_content_words(query)
        content_words = self._get_content_words(content)

        if not query_words:
            return 0.0

        # Find positions of query words in content
        positions = []
        for i, word in enumerate(content_words):
            if word in query_words:
                # Normalize position to [0, 1] where earlier positions get higher scores
                normalized_pos = 1.0 - (i / len(content_words)) if len(content_words) > 0 else 0
                positions.append(normalized_pos)

        if not positions:
            return 0.0

        # Average position score (higher for earlier matches)
        avg_position_score = sum(positions) / len(positions)

        # Weight by number of query words found
        found_ratio = len(positions) / len(query_words)
        position_score = avg_position_score * found_ratio

        return min(1.0, position_score)

    def _calculate_density_score(self, query: str, content: str) -> float:
        """Calculate score based on density of matching words in content"""
        query_words = set(self._get_content_words(query))
        content_words = self._get_content_words(content)

        if not query_words or not content_words:
            return 0.0

        matching_words = [word for word in content_words if word in query_words]
        density = len(matching_words) / len(content_words)

        # Boost score if matches are clustered together
        if len(matching_words) > 0:
            # Simple density boost for content that has concentrated matches
            density_score = min(1.0, density * 3)  # Boost by factor of 3, capped at 1.0
        else:
            density_score = 0.0

        return density_score

    def _get_content_words(self, text: str) -> List[str]:
        """Extract content words (non-stop words) from text"""
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if word not in self.stop_words and len(word) > 2]

    def calculate_relevance_for_chunks(self, query: str, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculate relevance scores for a list of content chunks
        """
        scored_chunks = []
        for chunk in chunks:
            content = chunk.get('content', '')
            relevance_score = self.calculate_relevance_score(query, content)

            scored_chunk = chunk.copy()
            scored_chunk['calculated_relevance_score'] = relevance_score
            scored_chunks.append(scored_chunk)

        # Sort by relevance score (descending)
        scored_chunks.sort(key=lambda x: x['calculated_relevance_score'], reverse=True)

        return scored_chunks

    def validate_relevance_threshold(self, query: str, content: str, threshold: float = 0.3) -> bool:
        """
        Check if content is relevant to query based on threshold
        """
        score = self.calculate_relevance_score(query, content)
        return score >= threshold

    def get_relevance_explanation(self, query: str, content: str) -> Dict[str, Any]:
        """
        Get detailed explanation of relevance calculation
        """
        query_normalized = self._normalize_text(query)
        content_normalized = self._normalize_text(content)

        keyword_score = self._calculate_keyword_match_score(query_normalized, content_normalized)
        semantic_score = self._calculate_semantic_similarity_score(query_normalized, content_normalized)
        position_score = self._calculate_position_score(query_normalized, content_normalized)
        density_score = self._calculate_density_score(query_normalized, content_normalized)

        query_words = self._get_content_words(query_normalized)
        content_words = self._get_content_words(content_normalized)
        matching_words = [word for word in query_words if word in content_words]

        final_score = (
            0.3 * keyword_score +
            0.4 * semantic_score +
            0.2 * position_score +
            0.1 * density_score
        )

        return {
            'final_score': final_score,
            'components': {
                'keyword_match': keyword_score,
                'semantic_similarity': semantic_score,
                'position': position_score,
                'density': density_score
            },
            'query_words': query_words,
            'content_words': content_words,
            'matching_words': matching_words,
            'query_word_count': len(query_words),
            'matching_word_count': len(matching_words)
        }