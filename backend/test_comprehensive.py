"""
Comprehensive test script for the RAG Agent API
"""

import asyncio
import requests
import json
import time
from typing import Dict, List
from src.utils.performance_monitor import performance_monitor
from src.services.response_validation import response_validation_service
from src.services.query_analyzer import query_analyzer_service, QueryType


def test_all_functionality():
    """
    Test all functionality of the RAG Agent API
    """
    base_url = "http://localhost:8000/api/v1"

    print("Testing comprehensive functionality of RAG Agent API...")
    print("Make sure the API server is running on http://localhost:8000")

    results = []

    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✓ Health check passed: {health_data['status']}")
            results.append({"test": "health", "status": "pass", "data": health_data})
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
            results.append({"test": "health", "status": "fail", "error": response.text})
    except Exception as e:
        print(f"   ✗ Health check error: {e}")
        results.append({"test": "health", "status": "error", "error": str(e)})

    # Test 2: Query type detection
    print("\n2. Testing query type detection...")
    sample_queries = [
        ("What is AI robotics?", QueryType.FACTUAL),
        ("Why is machine learning important?", QueryType.ANALYTICAL),
        ("Compare AI and ML", QueryType.COMPARATIVE),
        ("How to build a robot?", QueryType.PROCEDURAL)
    ]

    for query, expected_type in sample_queries:
        try:
            analysis = query_analyzer_service.analyze_query(query)
            match = analysis.query_type == expected_type
            print(f"   Query: '{query[:30]}...' -> {analysis.query_type.value} ({'✓' if match else '✗'})")
        except Exception as e:
            print(f"   ✗ Query analysis error for '{query}': {e}")

    # Test 3: Sample queries with different types
    print("\n3. Testing sample queries...")
    test_queries = [
        {
            "name": "Factual Query",
            "query": "What is artificial intelligence?",
            "max_results": 3,
            "include_citations": True,
            "temperature": 0.2
        },
        {
            "name": "Analytical Query",
            "query": "Why is machine learning important in robotics?",
            "max_results": 4,
            "include_citations": True,
            "temperature": 0.3
        },
        {
            "name": "Comparative Query",
            "query": "Compare supervised and unsupervised learning",
            "max_results": 3,
            "include_citations": True,
            "temperature": 0.3
        }
    ]

    for test_query in test_queries:
        print(f"   Testing {test_query['name']}: {test_query['query'][:40]}...")
        try:
            response = requests.post(
                f"{base_url}/query",
                json=test_query,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                response_data = response.json()
                print(f"     ✓ Status: {response.status_code}")
                print(f"     ✓ Answer length: {len(response_data['answer'])} chars")
                print(f"     ✓ Citations: {len(response_data['citations'])}")
                print(f"     ✓ Execution time: {response_data['execution_time']:.2f}s")

                # Validate response quality
                validation_report = response_validation_service.validate_response_quality(
                    type('obj', (object,), response_data)()
                )
                print(f"     ✓ Grounding validation: {validation_report['grounding_valid']}")
                print(f"     ✓ Quality score: {validation_report['quality_score']:.2f}")

                results.append({
                    "test": f"query_{test_query['name'].lower().replace(' ', '_')}",
                    "status": "pass",
                    "data": response_data,
                    "validation": validation_report
                })
            else:
                print(f"     ✗ Failed with status {response.status_code}: {response.text}")
                results.append({
                    "test": f"query_{test_query['name'].lower().replace(' ', '_')}",
                    "status": "fail",
                    "error": response.text
                })

        except Exception as e:
            print(f"     ✗ Error: {e}")
            results.append({
                "test": f"query_{test_query['name'].lower().replace(' ', '_')}",
                "status": "error",
                "error": str(e)
            })

    # Test 4: Error handling with invalid queries
    print("\n4. Testing error handling...")
    invalid_queries = [
        {"query": "", "name": "Empty query"},
        {"query": "a" * 1001, "name": "Too long query"},  # More than 1000 chars
        {"query": "valid query", "max_results": 25},  # Invalid max_results
    ]

    for invalid_query in invalid_queries:
        try:
            print(f"   Testing {invalid_query.get('name', 'invalid query')}...")
            response = requests.post(
                f"{base_url}/query",
                json=invalid_query,
                headers={"Content-Type": "application/json"}
            )

            print(f"     Response status: {response.status_code} (expected 422 for validation errors)")
            if response.status_code in [422, 400]:
                print(f"     ✓ Proper error handling for invalid input")
            else:
                print(f"     ? Unexpected status code: {response.status_code}")

        except Exception as e:
            print(f"     Error during invalid query test: {e}")

    # Test 5: Performance metrics
    print("\n5. Testing performance metrics...")
    try:
        summary = performance_monitor.get_metrics_summary()
        print(f"   ✓ Average response time: {summary['avg_response_time']:.2f}s")
        print(f"   ✓ P95 response time: {summary['p95_response_time']:.2f}s")
        print(f"   ✓ Success rate: {summary['success_rate']*100:.1f}%")
        print(f"   ✓ Throughput: {summary['throughput']:.2f} requests/min")
    except Exception as e:
        print(f"   ✗ Performance metrics error: {e}")

    return results


def print_test_summary(results: List[Dict]):
    """
    Print a summary of all test results
    """
    print("\n" + "="*60)
    print("COMPREHENSIVE TEST SUMMARY")
    print("="*60)

    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['status'] == 'pass')
    failed_tests = sum(1 for r in results if r['status'] == 'fail')
    error_tests = sum(1 for r in results if r['status'] == 'error')

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Errors: {error_tests}")

    if total_tests > 0:
        success_rate = (passed_tests / total_tests) * 100
        print(f"Success Rate: {success_rate:.1f}%")

    print("\nDetailed Results:")
    for result in results:
        status_icon = "✓" if result['status'] == 'pass' else "✗"
        print(f"  {status_icon} {result['test']}: {result['status']}")
        if 'error' in result:
            print(f"    Error: {result['error']}")


def test_rate_limiting():
    """
    Test rate limiting functionality
    """
    print("\n6. Testing rate limiting...")
    base_url = "http://localhost:8000/api/v1"

    # Send multiple requests rapidly to trigger rate limiting
    success_count = 0
    rate_limited_count = 0

    for i in range(150):  # Try to exceed the rate limit (default 100/min)
        try:
            response = requests.post(
                f"{base_url}/query",
                json={
                    "query": f"Test query {i} for rate limiting",
                    "max_results": 1,
                    "temperature": 0.1
                },
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 429:
                rate_limited_count += 1
                if rate_limited_count == 1:  # Only print first rate limit to avoid spam
                    print(f"   ✓ Rate limiting triggered: {response.status_code}")
                    print(f"     Headers: {dict(response.headers)}")
            elif response.status_code != 200:
                print(f"   Non-200 response: {response.status_code}")

        except Exception as e:
            print(f"   Error in rate limiting test: {e}")
            break

        # Small delay to not overwhelm the server completely
        time.sleep(0.01)

    print(f"   Requests processed: {success_count}")
    print(f"   Rate limited requests: {rate_limited_count}")


if __name__ == "__main__":
    print("Starting comprehensive RAG Agent API tests...")

    # Run all functionality tests
    results = test_all_functionality()

    # Print summary
    print_test_summary(results)

    # Test rate limiting specifically
    test_rate_limiting()

    print("\nComprehensive testing complete!")