"""
Basic test script for the RAG Agent API
"""

import asyncio
import requests
import json
from typing import Dict, Any
import time


def test_health_endpoint():
    """
    Test the health endpoint
    """
    print("Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/api/v1/health")
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False


def test_query_endpoint():
    """
    Test the query endpoint with a sample query
    """
    print("\nTesting query endpoint...")
    try:
        # Sample query
        query_data = {
            "query": "What is AI robotics?",
            "max_results": 3,
            "include_citations": True,
            "temperature": 0.3
        }

        response = requests.post(
            "http://localhost:8000/api/v1/query",
            json=query_data,
            headers={"Content-Type": "application/json"}
        )

        print(f"Query status: {response.status_code}")
        if response.status_code == 200:
            response_data = response.json()
            print(f"Query response: {json.dumps(response_data, indent=2)}")
            return True
        else:
            print(f"Query failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"Query test failed: {e}")
        return False


async def main():
    """
    Main test function
    """
    print("Starting RAG Agent API tests...")

    # Test health endpoint
    health_ok = test_health_endpoint()

    if health_ok:
        # Test query endpoint
        query_ok = test_query_endpoint()
        print(f"\nTest results: Health={health_ok}, Query={query_ok}")
    else:
        print("\nHealth check failed, skipping query test")


if __name__ == "__main__":
    # Note: This test requires the API server to be running
    # Start the server with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
    asyncio.run(main())