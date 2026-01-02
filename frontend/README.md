# RAG Chatbot Frontend

This is the frontend for the RAG (Retrieval-Augmented Generation) chatbot system. It provides a user-friendly interface for interacting with the documentation chatbot.

## Features

- Clean, responsive chat interface
- Real-time messaging with the AI assistant
- Toggle between regular RAG and advanced agent modes
- Typing indicators for better user experience
- Automatic scrolling to latest messages
- Link detection and formatting in responses

## Architecture

The frontend consists of:
- `index.html` - Main HTML structure for the chat interface
- `styles.css` - Styling for the chatbot UI
- `script.js` - JavaScript functionality for API integration
- `server.js` - Simple Express server for local development

## Setup

### Prerequisites

- Node.js installed on your system

### Installation

1. Install dependencies:
```bash
npm install
```

### Running the Frontend

1. Start the server:
```bash
npm start
```

2. Visit `http://localhost:3000` in your browser

## API Integration

The frontend communicates with the backend API using these endpoints:

- `/query` - Regular RAG queries for simple questions
- `/agent-query` - Agent-enhanced queries for complex reasoning

The API endpoints are called relative to the frontend, so when the backend serves the frontend (as in production), it will work correctly.

## Environment Configuration

For production deployments, you can configure the backend API URL through environment variables or build-time configuration. The `getApiBaseUrl()` function in `script.js` can be modified to read from environment variables.

## Deployment

The frontend is designed to work with the backend server. When deployed, the backend serves the frontend files directly, and API calls work using relative paths.

## Files

- `index.html` - Main chat interface HTML
- `styles.css` - Responsive CSS styling
- `script.js` - Client-side JavaScript logic
- `server.js` - Development server
- `package.json` - Node.js dependencies and scripts

## Development

To run in development mode:
```bash
npm run dev
```

## Troubleshooting

- If the chatbot doesn't connect to the backend, ensure the backend server is running and accessible
- Check browser console for JavaScript errors
- Verify that the backend API endpoints are accessible from the frontend