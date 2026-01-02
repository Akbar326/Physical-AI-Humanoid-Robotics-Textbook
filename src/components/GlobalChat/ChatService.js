// ChatService.js - API service for agent-only communication
import config from './config';

/**
 * Service to handle communication with the agent backend only
 * This service exclusively uses the agent endpoint, removing any basic RAG functionality
 */
class ChatService {
  constructor() {
    // Use the configured backend URL
    this.agentEndpoint = `${config.backendUrl}/agent-query`;
  }

  /**
   * Send a query to the agent backend (agent-only functionality)
   * @param {string} query - The user's query
   * @param {Object} options - Additional options for the query
   * @returns {Promise<Object>} The agent's response
   */
  async queryAgent(query, options = {}) {
    const requestBody = {
      query: query,
      top_k: options.topK || 5,
      session_id: options.sessionId || null,
      ...options.additionalParams
    };

    try {
      if (config.debug) {
        console.log('Attempting to connect to:', this.agentEndpoint); // Debug logging
        console.log('Request body:', requestBody); // Debug logging
      }

      // Add credentials and mode to handle cross-origin requests if needed
      const response = await fetch(this.agentEndpoint, {
        method: 'POST',
        mode: 'cors', // Enable CORS
        credentials: 'omit', // Don't send cookies unless needed
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
      });

      if (config.debug) {
        console.log('Response status:', response.status); // Debug logging
      }

      if (!response.ok) {
        const errorText = await response.text();
        console.error('HTTP error details:', response.status, errorText);
        throw new Error(`HTTP error! Status: ${response.status}, Details: ${errorText}`);
      }

      const data = await response.json();
      if (config.debug) {
        console.log('Response data:', data); // Debug logging
      }
      return data;
    } catch (error) {
      console.error('Error communicating with agent backend:', error);

      // Provide more specific error information
      if (error instanceof TypeError && error.message.includes('fetch')) {
        console.error('Network error - backend may be unreachable');
        throw new Error('Network error: Unable to reach the AI backend service. Please check if the backend server is running and accessible.');
      } else if (error.message.includes('HTTP error')) {
        throw error; // Re-throw HTTP errors as-is since they contain specific details
      } else {
        // Other errors (like parsing errors)
        throw new Error(`Error processing request: ${error.message}`);
      }
    }
  }
}

// Export a singleton instance
const chatService = new ChatService();
export default chatService;