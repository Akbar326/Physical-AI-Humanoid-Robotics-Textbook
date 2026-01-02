// Global configuration for the chatbot
const chatConfig = {
  // Backend API URL - update this to match your backend server
  // For development, use your local backend server
  // For production, use your deployed backend URL
  backendUrl: process.env.BACKEND_URL ||
             process.env.REACT_APP_BACKEND_URL ||
             process.env.NEXT_PUBLIC_BACKEND_URL ||
             'http://localhost:8000', // Default for local development

  // Timeout for API requests (in milliseconds)
  requestTimeout: 30000, // 30 seconds

  // Maximum number of messages to keep in history
  maxHistory: 50,

  // Whether to enable debug logging
  debug: process.env.NODE_ENV !== 'production'
};

export default chatConfig;