"""
Script to run the RAG Agent API server
"""

import uvicorn
import os
from main import app


def run_server():
    """
    Run the FastAPI server
    """
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))

    print(f"Starting RAG Agent API server on {host}:{port}")
    print("API documentation available at: http://localhost:8000/docs")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload during development
        log_level="info"
    )


if __name__ == "__main__":
    run_server()