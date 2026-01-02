"""
Basic search functionality wrapper service
"""

from typing import List, Dict, Any, Optional
import logging
import time
from config.settings import COHERE_API_KEY
from src.services.qdrant_helper import QdrantHelper
from src.models.validation import RetrievedChunk
from src.services.metadata_service import MetadataService

logger = logging.getLogger(__name__)

try:
    import cohere
    COHERE_AVAILABLE = True
except ImportError:
    logger.warning("Cohere library not available, using mock for embeddings")
    COHERE_AVAILABLE = False


class SearchService:
    """Service for performing search operations"""

    def __init__(self):
        self.qdrant_helper = QdrantHelper()
        self.metadata_service = MetadataService()
        if COHERE_AVAILABLE:
            self.cohere_client = cohere.Client(COHERE_API_KEY)
        else:
            self.cohere_client = None

    def embed_query(self, query_text: str) -> Optional[List[float]]:
        """Generate embedding for a query text"""
        if not COHERE_AVAILABLE or not self.cohere_client:
            logger.warning("Cohere not available, returning mock embedding")
            # Return a mock embedding for testing purposes
            return [0.1] * 1024  # Mock 1024-dimensional vector

        try:
            response = self.cohere_client.embed(
                texts=[query_text],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            return response.embeddings[0] if response.embeddings else None
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return None

    def search(self, query_text: str, top_k: int = 5) -> List[RetrievedChunk]:
        """Perform semantic search and return RetrievedChunk objects"""
        # Generate embedding for the query
        query_embedding = self.embed_query(query_text)
        if not query_embedding:
            logger.error("Failed to generate embedding for query")
            return []

        # Perform search in Qdrant
        search_results = self.qdrant_helper.search_vectors(query_embedding, top_k)
        if not search_results:
            logger.warning(f"No results found for query: {query_text}")
            return []

        # Convert results to RetrievedChunk objects
        retrieved_chunks = []
        for idx, result in enumerate(search_results):
            chunk = RetrievedChunk(
                chunk_id=result['chunk_id'],
                content=result['content'],
                source_url=result['source_url'],
                relevance_score=result['relevance_score'],
                position=result['position'] if 'position' in result else idx + 1,
                metadata=result['metadata']
            )
            retrieved_chunks.append(chunk)

        logger.info(f"Found {len(retrieved_chunks)} results for query: {query_text}")
        return retrieved_chunks

    def validate_search_functionality(self, test_query: str = "AI robotics") -> bool:
        """Validate that search functionality is working"""
        try:
            results = self.search(test_query, top_k=1)
            return len(results) > 0
        except Exception as e:
            logger.error(f"Error validating search functionality: {str(e)}")
            return False

    def batch_search(self, queries: List[str], top_k: int = 5) -> Dict[str, List[RetrievedChunk]]:
        """Perform multiple searches and return results for each"""
        results = {}
        for query in queries:
            results[query] = self.search(query, top_k)
        return results

    def search_with_metadata_validation(self, query_text: str, top_k: int = 5) -> Dict[str, Any]:
        """Perform search and include metadata validation results"""
        results = self.search(query_text, top_k)

        # Convert results to metadata format for validation
        search_results_metadata = []
        for result in results:
            metadata = {
                'chunk_id': result.chunk_id,
                'content': result.content,
                'url': result.source_url,
                'content_length': len(result.content),
                'extracted_urls': self.metadata_service._extract_urls(result.content),
                'extracted_emails': self.metadata_service._extract_emails(result.content)
            }
            search_results_metadata.append(metadata)

        # Validate metadata using the metadata service
        validation_summary = self.metadata_service.get_metadata_summary(search_results_metadata)

        # Get detailed validation results for each result
        detailed_validation_results = self.metadata_service.validate_search_result_metadata(search_results_metadata)

        return {
            'results': results,
            'metadata_accuracy': validation_summary['metadata_accuracy'],
            'metadata_validation_summary': validation_summary,
            'detailed_metadata_validation': detailed_validation_results,
            'query': query_text,
            'top_k': top_k
        }

    def get_search_performance_metrics(self, query_text: str, iterations: int = 5) -> Dict[str, Any]:
        """Get performance metrics for search operations"""
        total_time = 0
        successful_searches = 0

        for _ in range(iterations):
            start_time = time.time()
            try:
                results = self.search(query_text, top_k=1)
                end_time = time.time()
                total_time += (end_time - start_time)
                if results:
                    successful_searches += 1
            except Exception as e:
                logger.error(f"Search iteration failed: {str(e)}")
                continue

        avg_response_time = total_time / iterations if iterations > 0 else 0
        success_rate = successful_searches / iterations if iterations > 0 else 0

        return {
            'average_response_time': avg_response_time,
            'success_rate': success_rate,
            'total_time': total_time,
            'iterations': iterations
        }