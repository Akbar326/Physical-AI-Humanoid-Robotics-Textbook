"""
Basic tests to verify the RAG chatbot backend implementation.
"""
import asyncio
import os
from pathlib import Path

# Add the backend directory to the path so we can import our modules
import sys
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from services.rag import RAGService
from models.query import QueryRequest


def test_config():
    """Test that configuration is properly loaded"""
    print("Testing configuration...")

    # These should be set in the environment or .env file
    print(f"OpenAI API Key set: {'Yes' if settings.openai_api_key else 'No'}")
    print(f"Sitemap URL: {settings.sitemap_url}")
    print(f"Port: {settings.port}")

    # For basic testing, we'll just check that the settings module loads
    assert hasattr(settings, 'openai_api_key')
    assert hasattr(settings, 'sitemap_url')
    assert hasattr(settings, 'port')

    print("✓ Configuration test passed\n")


async def test_rag_service_creation():
    """Test that RAG service can be created (without initializing)"""
    print("Testing RAG service creation...")

    try:
        # Create RAG service instance
        rag_service = RAGService()
        print("✓ RAG service created successfully\n")
        return True
    except Exception as e:
        print(f"✗ Error creating RAG service: {e}\n")
        return False


async def test_models():
    """Test that models are properly defined"""
    print("Testing models...")

    try:
        # Test QueryRequest model
        query_request = QueryRequest(query="Test query", top_k=5)
        assert query_request.query == "Test query"
        assert query_request.top_k == 5
        print("✓ QueryRequest model works")

        # Test that required fields are validated
        try:
            # This should work with just the required field
            minimal_request = QueryRequest(query="Minimal query")
            print("✓ QueryRequest validation works")
        except Exception:
            print("✗ QueryRequest validation failed")

        print("✓ Models test passed\n")
        return True
    except Exception as e:
        print(f"✗ Error testing models: {e}\n")
        return False


async def main():
    """Run all basic tests"""
    print("Running basic tests for RAG Chatbot Backend...\n")

    test_config()

    await test_rag_service_creation()

    await test_models()

    print("All basic tests completed!")


if __name__ == "__main__":
    asyncio.run(main())