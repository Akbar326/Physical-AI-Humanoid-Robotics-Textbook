#!/usr/bin/env python3
"""
Script to run the RAG chatbot server.
"""

import uvicorn
import os
from config import settings


def main():
    """
    Main function to start the FastAPI server.
    """
    print("Starting RAG Chatbot Server...")
    print(f"Server will run on 0.0.0.0:{settings.port}")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=False,  # Set to True for development only
        log_level="info"
    )


if __name__ == "__main__":
    main()