# RagChatbot Component Documentation

## Overview
The RagChatbot component provides a chat interface for users to ask questions about the AI-Humanoid-Robotics textbook content and receive AI-generated responses based on the RAG (Retrieval-Augmented Generation) system.

## Features
- Real-time chat interface with message history
- Support for user queries and AI responses
- Loading indicators during API requests
- Error handling and user-friendly error messages
- Message history persistence using localStorage
- Auto-scrolling to latest messages
- Source citations for AI responses

## Props
The component does not accept any props as it is self-contained.

## File Structure
```
src/
└── components/
    └── RagChatbot/
        ├── RagChatbot.jsx          # Main chatbot component
        ├── RagChatbot.module.css   # Component-specific styles
        ├── ChatMessage.jsx         # Individual message component
        ├── ChatInput.jsx           # Input field and send button
        └── LoadingIndicator.jsx    # Loading state component
```

## API Integration
- Uses the RAG backend API at the configured base URL
- Supports environment variable configuration for API endpoint
- Implements retry logic for failed requests
- Handles various error scenarios gracefully

## Environment Configuration
Create a `.env` file with the following variable:
```
RAG_API_BASE_URL=http://localhost:8000
```

## Usage
To use the component in a Docusaurus page:

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

## Error Handling
The component handles various error scenarios:
- Network errors
- API timeouts
- Rate limiting (429 errors)
- Server errors (500+)
- Invalid queries (400)

## Accessibility
- Proper ARIA labels for interactive elements
- Keyboard navigation support
- Screen reader friendly

## Styling
- Responsive design for mobile and desktop
- Consistent with Docusaurus styling
- CSS Modules for scoped styling