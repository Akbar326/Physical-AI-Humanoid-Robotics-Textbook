# Quickstart Guide: Frontend-Backend Integration

## Prerequisites

- Node.js 16+ (for Docusaurus frontend)
- Python 3.11+ (for backend)
- Access to OpenAI API key
- Access to Qdrant vector database
- Existing RAG backend running
- Git for version control

## Setup Overview

The frontend-backend integration connects the Docusaurus-based book UI to the FastAPI RAG backend. The integration allows users to submit queries about book content and receive AI-generated responses.

## Backend Setup

1. **Ensure the RAG backend is running**
   ```bash
   cd backend
   pip install -r requirements.txt
   python run_server.py
   ```
   The backend should be available at `http://localhost:8000`

2. **Verify the backend is working**
   ```bash
   curl http://localhost:8000/api/v1/health
   ```

## Frontend Integration

1. **Navigate to the frontend directory**
   ```bash
   cd frontend  # or the directory containing your Docusaurus site
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Add the RAG query component to your Docusaurus site**
   - Create a new React component for the query interface
   - Add the component to relevant book pages
   - Configure the API endpoint to connect to the backend

4. **Start the Docusaurus development server**
   ```bash
   npm run start
   ```
   The frontend should be available at `http://localhost:3000`

## API Configuration

### Local Development Setup

The frontend will make requests to the backend API at `http://localhost:8000`. For local development:

1. **Environment Configuration**
   - No special configuration needed for local development
   - The API endpoint is hardcoded to connect to `http://localhost:8000`

2. **CORS Settings**
   - The backend already includes CORS middleware allowing requests from `http://localhost:3000`

### Query Component Integration

The RAG query component can be integrated into any Docusaurus page:

```jsx
import RagQueryForm from './components/RagQueryForm';

// In your Docusaurus page
function MyBookPage() {
  return (
    <div>
      <h1>My Book Page</h1>
      <p>Page content here...</p>
      <RagQueryForm />
    </div>
  );
}
```

## Using the Integrated System

### Submitting Queries

1. **Basic Queries**
   - Type your question in the query input field
   - Press Enter or click the submit button
   - Wait for the response to appear

2. **Context-Aware Queries**
   - Select text in the book content
   - The selected text will be automatically included in the query context
   - Submit your question about the selected text

### Expected Behavior

- Loading indicators will show during API requests
- Responses will appear in the results area
- Citations will be included in the response
- Error messages will display if requests fail

## Testing the Integration

1. **Verify API Connection**
   - Make sure the backend API is accessible at `http://localhost:8000`
   - Test the health endpoint: `curl http://localhost:8000/api/v1/health`

2. **Test Query Submission**
   - Submit a simple query from the frontend
   - Verify that the response appears in the UI
   - Check that response times are acceptable (< 5 seconds)

3. **Test Context-Aware Queries**
   - Select text in the book content
   - Submit a query about the selected text
   - Verify that the context is included in the request

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure the backend is running on `http://localhost:8000`
   - Verify CORS middleware is enabled in the backend

2. **API Connection Issues**
   - Check that the backend server is running
   - Verify the API endpoint configuration in the frontend
   - Check for firewall or network issues

3. **Slow Responses**
   - Verify that the Qdrant database is accessible
   - Check that the OpenAI API key is valid and has sufficient quota
   - Monitor system resources during requests

### Development Tips

- Use browser developer tools to inspect API requests and responses
- Check browser console for JavaScript errors
- Monitor backend logs for API request handling
- Test with various query types and lengths

## Next Steps

1. **Customize the UI**
   - Modify the query component styling to match your book's theme
   - Adjust the component placement on different pages

2. **Enhance Functionality**
   - Add query history functionality
   - Implement response caching
   - Add advanced query options

3. **Testing and Validation**
   - Test with various types of queries
   - Validate response accuracy
   - Verify error handling

## Configuration Options

### Frontend Configuration
- API endpoint URL (default: `http://localhost:8000`)
- Request timeout settings (default: 30 seconds)
- Default query parameters (temperature, max results, etc.)

### Backend Configuration
- OpenAI model selection
- Qdrant collection name
- Response formatting options
- Rate limiting settings