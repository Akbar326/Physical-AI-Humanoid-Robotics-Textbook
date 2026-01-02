import React, { useState, useEffect, useRef } from 'react';
import styles from './GlobalChat.module.css';

// SafeGlobalChat - A version that isolates all potential error sources
const SafeGlobalChat = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const messagesEndRef = useRef(null);

  // Initialize only after component mounts
  useEffect(() => {
    try {
      if (typeof window !== 'undefined') {
        const savedMessages = localStorage.getItem('globalChatMessages');
        if (savedMessages) {
          const parsedMessages = JSON.parse(savedMessages);
          if (Array.isArray(parsedMessages)) {
            setMessages(parsedMessages);
          }
        }
      }
      setIsInitialized(true);
    } catch (initError) {
      console.error('Error initializing SafeGlobalChat:', initError);
      setIsInitialized(true); // Still mark as initialized to show UI
    }
  }, []);

  // Save messages to localStorage whenever messages change
  useEffect(() => {
    try {
      if (typeof window !== 'undefined' && isInitialized) {
        localStorage.setItem('globalChatMessages', JSON.stringify(messages));
      }
    } catch (saveError) {
      console.error('Error saving messages to localStorage:', saveError);
    }
  }, [messages, isInitialized]);

  const scrollToBottom = () => {
    try {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    } catch (scrollError) {
      console.error('Error scrolling to bottom:', scrollError);
    }
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    if (isInitialized) {
      scrollToBottom();
    }
  }, [messages, isLoading, isInitialized]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading || !isInitialized) {
      return;
    }

    const userMessage = {
      id: Date.now(),
      sender: 'user',
      content: inputValue.trim(),
      timestamp: new Date()
    };

    // Add user message to chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    // Since we're not importing chatService to avoid initialization errors,
    // we'll simulate a response for now
    try {
      // Simulate a delay for "processing"
      await new Promise(resolve => setTimeout(resolve, 1000));

      const agentMessage = {
        id: Date.now() + 1,
        sender: 'agent',
        content: "I'm your AI assistant. The backend service is currently unavailable, but I'm working properly on the frontend.",
        timestamp: new Date(),
        sources: []
      };

      // Add agent response to chat
      setMessages(prev => [...prev, agentMessage]);
    } catch (err) {
      console.error('Error in simulated response:', err);
      setError('Sorry, I encountered an error while processing your request. Please try again.');

      const errorMessage = {
        id: Date.now() + 1,
        sender: 'agent',
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
        timestamp: new Date(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle Enter key for sending messages (without Shift for new line)
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  const formatMessage = (text) => {
    try {
      if (typeof text !== 'string') {
        return '';
      }
      // Convert URLs to clickable links
      const urlRegex = /(https?:\/\/[^\s]+)/g;
      const formattedText = text.replace(urlRegex, (url) => {
        return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
      });

      // Convert line breaks to <br> tags
      return formattedText.replace(/\n/g, '<br>');
    } catch (formatError) {
      console.error('Error formatting message:', formatError);
      return text || '';
    }
  };

  // Don't render anything until initialized to prevent errors
  if (!isInitialized) {
    return null;
  }

  return (
    <div className={styles.globalChatContainer}>
      {!isOpen ? (
        <button
          className={styles.toggleButton}
          onClick={toggleChat}
          aria-label="Open chat"
          aria-expanded="false"
        >
          💬
        </button>
      ) : (
        <div
          className={styles.chatWindow}
          role="dialog"
          aria-modal="true"
          aria-label="AI Assistant Chat"
        >
          <div className={styles.chatHeader}>
            <h3>AI Assistant</h3>
            <button
              className={styles.closeButton}
              onClick={closeChat}
              aria-label="Close chat"
              aria-expanded="true"
            >
              ×
            </button>
          </div>

          <div
            className={styles.messagesContainer}
            role="log"
            aria-live="polite"
            aria-label="Chat messages"
          >
            {messages.length === 0 && (
              <div className={styles.message + ' ' + styles.agentMessage}>
                <div
                  className={styles.messageContent}
                  dangerouslySetInnerHTML={{ __html: 'Hello! I\'m your AI assistant. Ask me anything about the textbook.' }}
                />
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${message.sender === 'user' ? styles.userMessage : styles.agentMessage}`}
                role="listitem"
              >
                <div
                  className={styles.messageContent}
                  dangerouslySetInnerHTML={{
                    __html: message.sender === 'user'
                      ? `<strong>You:</strong> ${formatMessage(message.content)}`
                      : `<strong>AI Assistant:</strong> ${formatMessage(message.content)}`
                  }}
                />
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.agentMessage}`}>
                <div className={styles.loadingIndicator} role="status" aria-label="AI Assistant is typing">
                  AI Assistant is typing...
                </div>
              </div>
            )}

            {error && (
              <div className={`${styles.message} ${styles.agentMessage} ${styles.errorMessage}`} role="alert">
                <div
                  className={styles.messageContent}
                  dangerouslySetInnerHTML={{ __html: `<strong>Error:</strong> ${formatMessage(error)}` }}
                />
              </div>
            )}

            <div ref={messagesEndRef} aria-hidden="true" />
          </div>

          <form onSubmit={handleSendMessage} className={styles.inputArea}>
            <input
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question..."
              disabled={isLoading}
              aria-label="Type your message"
              autoComplete="off"
              aria-describedby="chat-input-help"
            />
            <button
              type="submit"
              className={styles.sendButton}
              disabled={isLoading || !inputValue.trim()}
              aria-label="Send message"
            >
              ➤
            </button>
          </form>
          <div id="chat-input-help" className={styles.srOnly}>
            Press Enter to send message, Shift+Enter for new line
          </div>
        </div>
      )}
    </div>
  );
};

export default SafeGlobalChat;