"""
Qdrant service availability and health checks for the RAG Agent API
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from qdrant_client import QdrantClient
from config.settings import QDRANT_API_KEY, QDRANT_HOST, COLLECTION_NAME


logger = logging.getLogger(__name__)


class QdrantHealthService:
    """
    Service for checking Qdrant service availability and health
    """

    def __init__(self):
        self.client = QdrantClient(
            url=QDRANT_HOST,
            api_key=QDRANT_API_KEY,
            timeout=10
        )
        self.collection_name = COLLECTION_NAME
        self.last_health_check = None
        self.health_status = True
        self.last_error = None

    def check_availability(self) -> bool:
        """
        Check if Qdrant service is available
        """
        try:
            # Try to get collection info to verify connection
            collection_info = self.client.get_collection(self.collection_name)
            logger.info(f"Qdrant availability check passed. Collection '{self.collection_name}' has {collection_info.points_count} points")
            self.health_status = True
            self.last_health_check = datetime.now()
            self.last_error = None
            return True
        except Exception as e:
            logger.error(f"Qdrant availability check failed: {str(e)}")
            self.health_status = False
            self.last_health_check = datetime.now()
            self.last_error = str(e)
            return False

    def check_health_detailed(self) -> Dict[str, Any]:
        """
        Perform a detailed health check of the Qdrant service
        """
        health_info = {
            "service": "qdrant",
            "available": False,
            "healthy": False,
            "timestamp": datetime.now().isoformat(),
            "details": {}
        }

        try:
            # Check if we can connect and access the collection
            collection_info = self.client.get_collection(self.collection_name)

            health_info["available"] = True
            health_info["healthy"] = True
            health_info["details"] = {
                "collection_name": self.collection_name,
                "points_count": collection_info.points_count,
                "vector_size": collection_info.config.params.vectors.size if collection_info.config and collection_info.config.params and collection_info.config.params.vectors else None,
                "last_activity": getattr(collection_info, 'last_activity_timestamp', 'unknown')
            }

            logger.info(f"Qdrant health check passed: {collection_info.points_count} points in collection")

        except Exception as e:
            health_info["available"] = False
            health_info["healthy"] = False
            health_info["details"] = {
                "error": str(e),
                "error_type": type(e).__name__
            }
            logger.error(f"Qdrant health check failed: {str(e)}")

        return health_info

    def is_healthy(self) -> bool:
        """
        Check if the service is considered healthy
        """
        return self.health_status

    def get_last_error(self) -> Optional[str]:
        """
        Get the last error that occurred during health checks
        """
        return self.last_error

    def wait_for_availability(self, timeout: int = 30, interval: int = 1) -> bool:
        """
        Wait for Qdrant service to become available within the timeout period
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.check_availability():
                logger.info("Qdrant service became available")
                return True
            time.sleep(interval)

        logger.warning(f"Qdrant service did not become available within {timeout} seconds")
        return False


# Global instance for convenience
qdrant_health_service = QdrantHealthService()