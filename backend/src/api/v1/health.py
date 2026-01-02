"""
Health check endpoint for the RAG Agent API
"""

from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any
from ...services.qdrant_search import qdrant_search_service


router = APIRouter()


@router.get("/health", summary="Health Check")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify the API is running and services are available
    """
    # Check if Qdrant service is available
    qdrant_healthy = qdrant_search_service.check_health()

    status = "healthy" if qdrant_healthy else "degraded"

    return {
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "qdrant": qdrant_healthy
        }
    }