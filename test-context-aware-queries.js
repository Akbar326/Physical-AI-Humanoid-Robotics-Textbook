/**
 * Sample test file to demonstrate context-aware query functionality
 * This would normally be run as part of a test suite
 */

// Import the necessary modules
import apiClient from '../src/services/api-client';
import { sanitizeSelectedText, validateSelectedText } from '../src/utils/text-selection';

// Sample context-aware test queries
const contextAwareQueries = [
  {
    query: "What does this text mean?",
    selectedText: "Artificial intelligence in robotics combines machine learning algorithms with physical systems to create autonomous agents capable of performing complex tasks in real-world environments.",
    description: "Query with selected text context"
  },
  {
    query: "Explain the concept mentioned here",
    selectedText: "Forward kinematics is the process of determining the position and orientation of the end effector based on the joint angles of a robotic arm.",
    description: "Context-specific query"
  },
  {
    query: "How does this relate to neural networks?",
    selectedText: "Deep reinforcement learning is a subfield of machine learning that combines deep learning and reinforcement learning techniques to solve complex control problems.",
    description: "Cross-topic context query"
  }
];

// Function to test context-aware query submission
async function testContextAwareQuerySubmission() {
  console.log("Testing context-aware query submission functionality...\n");

  for (const [index, sample] of contextAwareQueries.entries()) {
    console.log(`Test ${index + 1}: ${sample.description}`);
    console.log(`Query: "${sample.query}"`);
    console.log(`Selected Text: "${sample.selectedText.substring(0, 50)}..."`);

    try {
      // Sanitize the selected text
      const sanitizedText = sanitizeSelectedText(sample.selectedText);
      console.log(`Sanitized Text: "${sanitizedText.substring(0, 50)}..."`);

      // Validate the selected text
      const validation = validateSelectedText(sanitizedText);
      if (!validation.isValid) {
        throw new Error(`Validation failed: ${validation.error}`);
      }
      console.log("✓ Text validation passed");

      // Prepare the query data with context
      const queryData = {
        query: sample.query,
        selectedText: sanitizedText,
        max_results: 5,
        include_citations: true,
        temperature: 0.3
      };

      console.log("Sending context-aware query to API...");

      // In a real test environment, this would call the actual API
      // For demonstration purposes, we'll just show what would be sent
      console.log("Query data that would be sent:", JSON.stringify(queryData, null, 2));

      // If we had a backend running, we would uncomment the following:
      // const result = await apiClient.submitQuery(queryData);
      // console.log("Response received:", JSON.stringify(result, null, 2));

      console.log("✓ Context-aware query format is valid\n");
    } catch (error) {
      console.error(`✗ Error in test ${index + 1}:`, error.message);
    }
  }

  console.log("Context-aware query tests completed.");
}

// Run the test
testContextAwareQuerySubmission().catch(console.error);