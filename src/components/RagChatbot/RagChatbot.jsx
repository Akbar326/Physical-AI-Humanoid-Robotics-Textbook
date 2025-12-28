import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import LoadingIndicator from './LoadingIndicator';
import { submitQuery, retryApiCall } from '@site/src/services/api/rag-api';
import styles from './RagChatbot.module.css';

/**
 * Main RAG Chatbot component
 * Provides a chat interface for users to ask questions about book content
 * and receive AI-generated responses based on the RAG system
 */
const RagChatbot = () => {
  // State for chat messages, loading state, and errors
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);

  // Reference for auto-scrolling to the latest message
  const messagesEndRef = useRef(null);

  // Load chat history from localStorage on component mount
  useEffect(() => {
    const savedMessages = localStorage.getItem('ragChatMessages');
    const savedSessionId = localStorage.getItem('ragChatSessionId');

    if (savedMessages) {
      try {
        const parsedMessages = JSON.parse(savedMessages);
        setMessages(parsedMessages);
      } catch (e) {
        console.error('Failed to parse saved messages:', e);
        // If parsing fails, start with empty messages
        setMessages([]);
      }
    }

    if (savedSessionId) {
      setSessionId(savedSessionId);
    }
  }, []);

  // Save chat history to localStorage whenever messages change
  useEffect(() => {
    localStorage.setItem('ragChatMessages', JSON.stringify(messages));
  }, [messages]);

  // Save session ID to localStorage whenever it changes
  useEffect(() => {
    if (sessionId) {
      localStorage.setItem('ragChatSessionId', sessionId);
    }
  }, [sessionId]);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Handle user query submission
  const handleQuerySubmit = async (query) => {
    if (!query.trim()) return;

    try {
      // Add user message to the chat
      const userMessage = {
        id: Date.now().toString(),
        sender: 'user',
        content: query,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, userMessage]);
      setIsLoading(true);
      setError(null);

      // Submit query to RAG backend with retry mechanism
      const response = await retryApiCall(() => submitQuery(query, sessionId), 2, 1000);

      // Update session ID if returned
      if (response.session_id && !sessionId) {
        setSessionId(response.session_id);
      }

      // Add assistant response to the chat
      const assistantMessage = {
        id: `assistant-${Date.now()}`,
        sender: 'assistant',
        content: response.response,
        sources: response.sources || [],
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      // Add error message to the chat
      setError(err.message);
      const errorMessage = {
        id: `error-${Date.now()}`,
        sender: 'system',
        content: `Error: ${err.message}`,
        timestamp: new Date(),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to clear chat history
  const clearChatHistory = () => {
    setMessages([]);
    localStorage.removeItem('ragChatMessages');
  };

  return (
    <div className={styles.chatContainer} role="region" aria-label="AI Assistant Chat Interface">
      <div className={styles.chatHeader}>
        <h3>AI Assistant</h3>
        <p>Ask questions about the AI-Humanoid-Robotics textbook</p>
        {messages.length > 0 && (
          <button
            onClick={clearChatHistory}
            className={styles.clearHistoryButton}
            aria-label="Clear chat history"
          >
            Clear History
          </button>
        )}
      </div>

      <div
        className={styles.chatMessages}
        role="list"
        aria-label="Chat messages"
        aria-live="polite"
        aria-relevant="additions"
      >
        {messages.length === 0 ? (
          <div className={styles.welcomeMessage} role="status" aria-live="polite">
            <p>Hello! I'm your AI assistant for the AI-Humanoid-Robotics textbook.</p>
            <p>Ask me any questions about the content, and I'll provide answers based on the book.</p>
          </div>
        ) : (
          messages.map((message) => (
            <ChatMessage
              key={message.id}
              message={message.content}
              sender={message.sender}
              timestamp={message.timestamp}
              sources={message.sources}
              isError={message.isError}
            />
          ))
        )}

        {isLoading && <LoadingIndicator />}
        <div ref={messagesEndRef} aria-hidden="true" />
      </div>

      <div className={styles.chatInputContainer}>
        <ChatInput onQuerySubmit={handleQuerySubmit} disabled={isLoading} />
        {error && (
          <div className={styles.errorMessage} role="alert" aria-live="assertive">
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default RagChatbot;