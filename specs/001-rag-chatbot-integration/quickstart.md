# Quickstart: RAG Chatbot Integration

## Prerequisites

- Node.js >= 18.0.0
- Docusaurus project set up and running
- FastAPI RAG backend running at configured endpoint
- Basic knowledge of React and Docusaurus

## Setup Steps

### 1. Environment Configuration

Create or update your `.env` file with the API configuration:

```bash
RAG_API_BASE_URL=http://localhost:8000
# For production deployment, change to your production API URL
```

### 2. Component Installation

Create the chatbot component directory and files:

```bash
mkdir -p src/components/RagChatbot
touch src/components/RagChatbot/RagChatbot.jsx
touch src/components/RagChatbot/RagChatbot.module.css
touch src/components/RagChatbot/ChatMessage.jsx
touch src/components/RagChatbot/ChatInput.jsx
touch src/components/RagChatbot/LoadingIndicator.jsx
```

### 3. API Service Setup

Create the API service:

```bash
mkdir -p src/services/api
touch src/services/api/rag-api.js
```

### 4. Basic Implementation

1. Implement the RagChatbot component with state management
2. Create API service functions to connect to the RAG backend
3. Add the component to your Docusaurus pages where needed

### 5. Testing

1. Start your Docusaurus development server: `npm start`
2. Start your RAG backend: `cd backend && python run_server.py`
3. Navigate to a page with the chatbot component
4. Test sending queries and receiving responses

## Usage Example

To add the chatbot to a Docusaurus page:

```jsx
import RagChatbot from '@site/src/components/RagChatbot/RagChatbot';

function MyPage() {
  return (
    <div>
      <h1>My Page Content</h1>
      <p>Some content here...</p>
      <RagChatbot />
    </div>
  );
}
```

## Troubleshooting

- If the chatbot doesn't connect to the API, verify your `RAG_API_BASE_URL` is correct
- Check browser console for any error messages
- Ensure your backend server is running and accessible
- Verify CORS settings if experiencing connection issues