import React, { useState, useEffect, useRef } from 'react';
import styles from './GlobalChat.module.css';
import chatService from './ChatService';

const GlobalChat = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState(() => {
    // Initialize messages from localStorage if available
    if (typeof window !== 'undefined') {
      const savedMessages = localStorage.getItem('globalChatMessages');
      return savedMessages ? JSON.parse(savedMessages) : [];
    }
    return [];
  });
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Save messages to localStorage whenever messages change
  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('globalChatMessages', JSON.stringify(messages));
    }
  }, [messages]);

  // Scroll to bottom of messages when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

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

    if (!inputValue.trim() || isLoading) {
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

    try {
      // Call the agent service
      const response = await chatService.queryAgent(userMessage.content);

      const agentMessage = {
        id: Date.now() + 1,
        sender: 'agent',
        content: response.answer,
        timestamp: new Date(),
        sources: response.sources || []
      };

      // Add agent response to chat
      setMessages(prev => [...prev, agentMessage]);
    } catch (err) {
      console.error('Error getting agent response:', err);
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
    // Convert URLs to clickable links
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const formattedText = text.replace(urlRegex, (url) => {
      return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
    });

    // Convert line breaks to <br> tags
    return formattedText.replace(/\n/g, '<br>');
  };

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

export default GlobalChat;