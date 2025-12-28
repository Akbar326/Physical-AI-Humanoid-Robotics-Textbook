"""
Qdrant search service for the RAG Agent API
"""

import logging
from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct, SearchRequest
from config.settings import QDRANT_API_KEY, QDRANT_HOST, COLLECTION_NAME
from ..models.search import RetrievedContext, SearchQuery


logger = logging.getLogger(__name__)

# Initialize Qdrant client
qdrant_client = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY,
    timeout=10
)


class QdrantSearchService:
    """
    Service class for handling search operations with Qdrant
    """

    def __init__(self):
        self.client = qdrant_client
        self.collection_name = COLLECTION_NAME

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text using Cohere
        """
        try:
            import cohere
            from config.settings import COHERE_API_KEY

            co = cohere.Client(COHERE_API_KEY)
            response = co.embed(
                texts=[text],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            return response.embeddings[0]
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise

    def search(self, search_query: SearchQuery) -> List[RetrievedContext]:
        """
        Search for relevant content in Qdrant based on the query
        """
        try:
            # Generate embedding for the search query
            query_embedding = self.embed_text(search_query.text)

            # Perform vector search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=search_query.top_k,
                with_payload=True
            )

            results = []
            for result in search_results:
                payload = result.payload
                results.append(RetrievedContext(
                    content=payload.get('content', ''),
                    url=payload.get('url', ''),
                    title=payload.get('title', ''),
                    score=result.score
                ))

            logger.info(f"Found {len(results)} results for query: {search_query.text[:50]}...")
            return results

        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            raise

    def search_by_text(self, query_text: str, top_k: int = 5) -> List[RetrievedContext]:
        """
        Convenience method to search by text directly
        """
        search_query = SearchQuery(text=query_text, top_k=top_k)
        return self.search(search_query)

    def check_health(self) -> bool:
        """
        Check if Qdrant service is available
        """
        try:
            # Try to get collection info to verify connection
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(f"Qdrant health check passed. Collection '{self.collection_name}' has {collection_info.points_count} points")
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {str(e)}")
            return False


# Global instance for convenience
qdrant_search_service = QdrantSearchService()