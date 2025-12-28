"""
Qdrant connection and validation helper service
"""

from typing import List, Dict, Any, Optional
import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
from config.settings import QDRANT_API_KEY, QDRANT_HOST, COLLECTION_NAME

logger = logging.getLogger(__name__)


class QdrantHelper:
    """Helper class for Qdrant operations and validation"""

    def __init__(self):
        self.client = QdrantClient(
            url=QDRANT_HOST,
            api_key=QDRANT_API_KEY,
            timeout=10
        )
        self.collection_name = COLLECTION_NAME

    def validate_connection(self) -> bool:
        """Validate that we can connect to Qdrant"""
        try:
            # Try to get collections list to test connection
            collections = self.client.get_collections()
            logger.info(f"Successfully connected to Qdrant. Found {len(collections.collections)} collections")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {str(e)}")
            return False

    def collection_exists(self) -> bool:
        """Check if the expected collection exists"""
        try:
            collections = self.client.get_collections()
            collection_names = [coll.name for coll in collections.collections]
            return self.collection_name in collection_names
        except Exception as e:
            logger.error(f"Error checking collection existence: {str(e)}")
            return False

    def get_collection_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the collection"""
        try:
            if not self.collection_exists():
                return None
            collection_info = self.client.get_collection(self.collection_name)
            return {
                'name': collection_info.name,
                'vector_size': collection_info.config.params.vectors.size,
                'distance': collection_info.config.params.vectors.distance,
                'points_count': collection_info.points_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return None

    def search_vectors(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform vector search in the collection"""
        try:
            search_results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=top_k,
                with_payload=True,
                with_vectors=False
            )

            results = []
            for idx, result in enumerate(search_results.points):
                results.append({
                    'chunk_id': result.id,
                    'content': result.payload.get('content', ''),
                    'source_url': result.payload.get('url', ''),
                    'relevance_score': result.score,
                    'position': idx + 1,
                    'metadata': result.payload
                })

            return results
        except Exception as e:
            logger.error(f"Error performing vector search: {str(e)}")
            return []

    def get_all_points_count(self) -> int:
        """Get the total number of points in the collection"""
        try:
            if not self.collection_exists():
                return 0
            collection_info = self.client.get_collection(self.collection_name)
            return collection_info.points_count
        except Exception as e:
            logger.error(f"Error getting points count: {str(e)}")
            return 0

    def validate_vector_dimensions(self) -> bool:
        """Validate that the collection has the expected vector dimensions"""
        try:
            collection_info = self.get_collection_info()
            if not collection_info:
                return False
            # Assuming Cohere embeddings have 1024 dimensions (for embed-english-v3.0)
            expected_dimensions = 1024
            return collection_info['vector_size'] == expected_dimensions
        except Exception as e:
            logger.error(f"Error validating vector dimensions: {str(e)}")
            return False

    def test_search_capability(self, test_query: List[float], top_k: int = 1) -> bool:
        """Test if search functionality is working"""
        try:
            results = self.search_vectors(test_query, top_k)
            return len(results) > 0
        except Exception as e:
            logger.error(f"Error testing search capability: {str(e)}")
            return False