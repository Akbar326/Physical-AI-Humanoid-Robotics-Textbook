#!/usr/bin/env python3
"""
Script for pre-generating embeddings from a sitemap and building the vector store.
This script can be run independently to build the vector store before starting the server.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.rag import RAGService
from config import settings
from utils.logging import app_logger


async def main():
    """
    Main function to run the ingestion process.
    """
    print("Starting RAG ingestion process...")

    # Check that required environment variables are set
    if not settings.openai_api_key:
        print("Error: OPENAI_API_KEY environment variable is required")
        sys.exit(1)

    if not settings.sitemap_url:
        print("Error: SITEMAP_URL environment variable is required")
        sys.exit(1)

    print(f"Using sitemap URL: {settings.sitemap_url}")

    try:
        # Initialize the RAG service
        rag_service = RAGService()

        # Run the ingestion process
        await rag_service.ingest_sitemap(settings.sitemap_url)

        print("Ingestion completed successfully!")
        print(f"Vector store saved to: {rag_service.vector_store_path}")
        print(f"Documents saved to: {rag_service.documents_path}")

    except Exception as e:
        app_logger.error(f"Ingestion failed: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())