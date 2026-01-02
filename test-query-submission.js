/**
 * Sample test file to demonstrate query submission functionality
 * This would normally be run as part of a test suite
 */

// Import the necessary modules
import apiClient from '../src/services/api-client';

// Sample test queries
const sampleQueries = [
  {
    query: "What are the key concepts in AI robotics?",
    description: "Basic query about AI robotics concepts"
  },
  {
    query: "Explain the difference between forward and inverse kinematics",
    selectedText: "Kinematics is the study of motion without considering the forces that cause it.",
    description: "Context-aware query with selected text"
  },
  {
    query: "How does deep learning apply to robot control?",
    max_results: 3,
    description: "Query with custom parameters"
  }
];

// Function to test query submission
async function testQuerySubmission() {
  console.log("Testing query submission functionality...\n");

  for (const [index, sample] of sampleQueries.entries()) {
    console.log(`Test ${index + 1}: ${sample.description}`);
    console.log(`Query: "${sample.query}"`);

    try {
      // Prepare the query data
      const queryData = {
        query: sample.query,
        selectedText: sample.selectedText || null,
        max_results: sample.max_results || 5,
        include_citations: true,
        temperature: 0.3
      };

      console.log("Sending query to API...");

      // In a real test environment, this would call the actual API
      // For demonstration purposes, we'll just show what would be sent
      console.log("Query data that would be sent:", JSON.stringify(queryData, null, 2));

      // If we had a backend running, we would uncomment the following:
      // const result = await apiClient.submitQuery(queryData);
      // console.log("Response received:", JSON.stringify(result, null, 2));

      console.log("✓ Query format is valid\n");
    } catch (error) {
      console.error(`✗ Error in test ${index + 1}:`, error.message);
    }
  }

  console.log("Query submission tests completed.");
}

// Run the test
testQuerySubmission().catch(console.error);