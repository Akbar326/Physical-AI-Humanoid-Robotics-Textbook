// Chatbot functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const agentMode = document.getElementById('agent-mode');
    const typingIndicator = document.getElementById('typing-indicator');

    // Add welcome message if there are no messages yet
    if (chatMessages.children.length <= 1) { // Account for initial bot message
        addMessage('bot', 'Hello! I\'m your documentation assistant. Ask me anything about the documentation. You can also toggle "Use Advanced Agent" for more sophisticated responses.');
    }

    // Function to add a message to the chat
    function addMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = `<strong>${sender === 'user' ? 'You:' : 'AI Assistant:'}</strong> ${formatMessage(text)}`;

        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to format message text (convert URLs to links, handle line breaks)
    function formatMessage(text) {
        // Convert URLs to clickable links
        text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
        // Convert line breaks to <br> tags
        text = text.replace(/\n/g, '<br>');
        return text;
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        typingIndicator.style.display = 'block';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to hide typing indicator
    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    // Function to get the API base URL - use relative path for same-origin or environment variable for production
    function getApiBaseUrl() {
        // In production, you might set a specific backend URL via environment or build process
        // For now, we'll use a relative path which works when frontend is served from the same origin
        return '';
    }

    // Function to send message to backend
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to UI
        addMessage('user', message);
        userInput.value = '';
        sendButton.disabled = true;

        // Show typing indicator
        showTypingIndicator();

        try {
            // Determine which endpoint to use based on agent mode
            const endpoint = agentMode.checked ? getApiBaseUrl() + '/agent-query' : getApiBaseUrl() + '/query';
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: message,
                    top_k: 5  // Number of sources to retrieve
                })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();

            // Hide typing indicator
            hideTypingIndicator();

            // Add bot response to UI
            addMessage('bot', data.answer);

            // Log sources in console for reference
            if (data.sources && data.sources.length > 0) {
                console.log('Sources:', data.sources);
            }
        } catch (error) {
            console.error('Error sending message:', error);

            // Hide typing indicator
            hideTypingIndicator();

            // Add error message to UI
            addMessage('bot', 'Sorry, I encountered an error while processing your request. Please try again.');
        } finally {
            sendButton.disabled = false;
        }
    }

    // Event listener for send button
    sendButton.addEventListener('click', sendMessage);

    // Event listener for Enter key in input field
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Event listener for agent mode toggle - just for UI feedback
    agentMode.addEventListener('change', function() {
        if (this.checked) {
            console.log('Advanced agent mode enabled');
        } else {
            console.log('Regular RAG mode enabled');
        }
    });
});