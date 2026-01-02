"""
Test script for the RAG Agent API with sample queries
"""

import asyncio
import requests
import json
import time
from typing import Dict, List
from src.services.response_validation import response_validation_service
from src.utils.performance_monitor import performance_monitor


def run_sample_queries():
    """
    Run sample queries to test the API functionality
    """
    base_url = "http://localhost:8000/api/v1"

    # Sample queries for testing
    sample_queries = [
        {
            "query": "What is AI robotics?",
            "max_results": 3,
            "include_citations": True,
            "temperature": 0.3
        },
        {
            "query": "Explain the fundamentals of humanoid robots",
            "max_results": 5,
            "include_citations": True,
            "temperature": 0.2
        },
        {
            "query": "What are the applications of physical AI?",
            "max_results": 4,
            "include_citations": True,
            "temperature": 0.3
        }
    ]

    print("Running sample queries to test the RAG Agent API...")
    results = []

    for i, query_data in enumerate(sample_queries):
        print(f"\n--- Test Query {i+1} ---")
        print(f"Query: {query_data['query']}")

        try:
            response = requests.post(
                f"{base_url}/query",
                json=query_data,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                response_data = response.json()
                print(f"Status: {response.status_code}")
                print(f"Answer: {response_data['answer'][:200]}...")
                print(f"Citations: {len(response_data['citations'])} sources")
                print(f"Execution Time: {response_data['execution_time']:.2f}s")

                # Validate response grounding
                is_valid = response_validation_service.validate_response_grounding(
                    query_data['query'],
                    response_data['answer'],
                    response_data['retrieved_contexts']
                )
                print(f"Grounding Valid: {is_valid}")

                # Validate response time
                time_valid = response_validation_service.validate_response_time(
                    type('obj', (object,), response_data)(),  # Convert dict to object
                    max_time=5.0
                )
                print(f"Time Valid (<5s): {time_valid}")

                results.append({
                    "query": query_data['query'],
                    "status": response.status_code,
                    "execution_time": response_data['execution_time'],
                    "grounding_valid": is_valid,
                    "time_valid": time_valid,
                    "citations_count": len(response_data['citations'])
                })
            else:
                print(f"Failed with status {response.status_code}: {response.text}")
                results.append({
                    "query": query_data['query'],
                    "status": response.status_code,
                    "error": response.text
                })

        except Exception as e:
            print(f"Error running query: {e}")
            results.append({
                "query": query_data['query'],
                "error": str(e)
            })

    return results


def print_test_summary(results: List[Dict]):
    """
    Print a summary of the test results
    """
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    total_tests = len(results)
    successful_tests = sum(1 for r in results if 'error' not in r and r.get('status') == 200)
    grounding_valid = sum(1 for r in results if r.get('grounding_valid', False))
    time_valid = sum(1 for r in results if r.get('time_valid', False))

    print(f"Total Tests Run: {total_tests}")
    print(f"Successful Tests: {successful_tests}")
    print(f"Response Grounding Valid: {grounding_valid}/{total_tests}")
    print(f"Response Time Valid (<5s): {time_valid}/{total_tests}")

    if total_tests > 0:
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        print(f"Grounding Valid Rate: {(grounding_valid/total_tests)*100:.1f}%")
        print(f"Time Valid Rate: {(time_valid/total_tests)*100:.1f}%")

    # Print performance summary
    successful_results = [r for r in results if 'execution_time' in r]
    if successful_results:
        avg_time = sum(r['execution_time'] for r in successful_results) / len(successful_results)
        print(f"Average Response Time: {avg_time:.2f}s")
        print(f"Fastest Response: {min(r['execution_time'] for r in successful_results):.2f}s")
        print(f"Slowest Response: {max(r['execution_time'] for r in successful_results):.2f}s")

    print("\nDetailed Results:")
    for i, result in enumerate(results):
        status_icon = "✓" if result.get('status') == 200 else "✗"
        print(f"  {status_icon} Query {i+1}: {result.get('query', 'N/A')[:50]}...")
        if 'error' in result:
            print(f"    Error: {result['error']}")
        else:
            print(f"    Status: {result.get('status')}, Time: {result.get('execution_time', 0):.2f}s, "
                  f"Grounding: {'✓' if result.get('grounding_valid') else '✗'}, "
                  f"Time Valid: {'✓' if result.get('time_valid') else '✗'}")


def test_performance_metrics():
    """
    Test the performance monitoring functionality
    """
    print("\n" + "="*60)
    print("PERFORMANCE METRICS")
    print("="*60)

    try:
        summary = performance_monitor.get_metrics_summary()
        print(f"Average Response Time: {summary['avg_response_time']:.2f}s")
        print(f"95th Percentile Response Time: {summary['p95_response_time']:.2f}s")
        print(f"Success Rate: {summary['success_rate']*100:.1f}%")
        print(f"Throughput: {summary['throughput']:.2f} requests/min")
    except Exception as e:
        print(f"Error getting performance metrics: {e}")


if __name__ == "__main__":
    print("Starting RAG Agent API tests...")
    print("Note: Make sure the API server is running on http://localhost:8000")

    # Run sample queries
    results = run_sample_queries()

    # Print test summary
    print_test_summary(results)

    # Test performance metrics
    test_performance_metrics()

    print("\nTesting complete!")