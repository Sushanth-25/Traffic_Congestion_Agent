// Configuration
const CONFIG = {
    LANGFLOW_API_URL: LANGFLOW_CONFIG.apiUrl,
    FLOW_ID: LANGFLOW_CONFIG.flowId,
    APPLICATION_TOKEN: LANGFLOW_CONFIG.applicationToken,
    ORGANIZATION_ID: LANGFLOW_CONFIG.organizationId,
    TWEAKS: LANGFLOW_CONFIG.tweaks || {}
};

// State management
const state = {
    isProcessing: false,
    messageHistory: []
};

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const connectionStatus = document.getElementById('connection-status');

// Initialize the application
function init() {
    // Setup event listeners
    chatForm.addEventListener('submit', handleSubmit);
    
    // Auto-resize textarea
    userInput.addEventListener('input', autoResizeTextarea);
    
    // Handle Enter key (send on Enter, new line on Shift+Enter)
    userInput.addEventListener('keydown', handleKeyPress);
    
    // Focus on input
    userInput.focus();
    
    console.log('Traffic AI Assistant initialized');
}

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();
    
    const message = userInput.value.trim();
    
    if (!message || state.isProcessing) return;
    
    // Clear input
    userInput.value = '';
    autoResizeTextarea();
    
    // Send message
    await sendMessage(message);
}

// Send message to Langflow
async function sendMessage(message) {
    // Add user message to chat
    addMessageToChat(message, 'user');
    
    // Set processing state
    state.isProcessing = true;
    updateSendButton(true);
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        // Call Langflow API
        const response = await callLangflowAPI(message);
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add AI response to chat
        if (response && response.outputs && response.outputs.length > 0) {
            const output = response.outputs[0];
            const aiMessage = extractMessageFromOutput(output);
            addMessageToChat(aiMessage, 'ai');
        } else {
            throw new Error('Invalid response format from Langflow');
        }
        
        // Update connection status
        updateConnectionStatus(true);
        
    } catch (error) {
        console.error('Error sending message:', error);
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Show error message
        addMessageToChat(
            `I'm sorry, I encountered an error: ${error.message}. Please check your Langflow connection and try again.`,
            'error'
        );
        
        // Update connection status
        updateConnectionStatus(false);
    } finally {
        // Reset processing state
        state.isProcessing = false;
        updateSendButton(false);
        userInput.focus();
    }
}

// Call Langflow API
async function callLangflowAPI(message) {
    // Build endpoint with optional API key as query parameter
    let endpoint = `${CONFIG.LANGFLOW_API_URL}/${CONFIG.FLOW_ID}`;
    
    // For local LangFlow, add API key as query param if no Bearer token will be used
    if (CONFIG.APPLICATION_TOKEN && !CONFIG.APPLICATION_TOKEN.startsWith('Bearer')) {
        endpoint += `?x-api-key=${CONFIG.APPLICATION_TOKEN}`;
    }
    
    // Generate unique session ID for this conversation
    const sessionId = crypto.randomUUID();
    
    // Build tweaks with the user's message
    const tweaks = {
        ...CONFIG.TWEAKS,
        "ChatInput-oxbHs": {
            ...CONFIG.TWEAKS["ChatInput-oxbHs"],
            "input_value": message,
            "session_id": sessionId
        }
    };
    
    const payload = {
        output_type: "chat",
        input_type: "chat",
        tweaks: tweaks
    };
    
    // Add session_id at root level for tracking
    payload.session_id = sessionId;
    
   // Headers for local or cloud Langflow
    const headers = {
        'Content-Type': 'application/json'
    };

    // Add authentication only if token is provided (for cloud/authenticated local)
    if (CONFIG.APPLICATION_TOKEN) {
        headers['Authorization'] = `Bearer ${CONFIG.APPLICATION_TOKEN}`;
    }

    // Add org header only if provided (for DataStax cloud)
    if (CONFIG.ORGANIZATION_ID) {
        headers['X-DataStax-Current-Org'] = CONFIG.ORGANIZATION_ID;
    }

    const response = await fetch(endpoint, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(payload)
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// Extract message from Langflow output
function extractMessageFromOutput(output) {
    console.log('Raw output received:', JSON.stringify(output, null, 2)); // Debug log
    console.log('Available keys:', Object.keys(output));
    
    // Handle if full response was passed instead of just outputs[0]
    if (output.outputs && output.outputs.length > 0) {
        console.log('⚠️ Full response passed, extracting outputs[0]');
        output = output.outputs[0];
    }
    
    // Direct extraction: outputs[0].results.message.text
    if (output.results && output.results.message && output.results.message.text) {
        console.log('✓ Found text at: output.results.message.text');
        return output.results.message.text;
    }
    
    // Try nested in data object
    if (output.results && output.results.message && output.results.message.data && output.results.message.data.text) {
        console.log('✓ Found text at: output.results.message.data.text');
        return output.results.message.data.text;
    }
    
    // Alternative: outputs.message.message
    if (output.outputs && output.outputs.message && output.outputs.message.message) {
        console.log('✓ Found text at: output.outputs.message.message');
        return output.outputs.message.message;
    }
    
    // Alternative: artifacts.message
    if (output.artifacts && typeof output.artifacts.message === 'string') {
        console.log('✓ Found text at: output.artifacts.message');
        return output.artifacts.message;
    }
    
    // Alternative: messages[0].message
    if (output.messages && output.messages[0] && output.messages[0].message) {
        console.log('✓ Found text at: output.messages[0].message');
        return output.messages[0].message;
    }
    
    // No valid path found
    console.error('✗ Failed to extract text from output.');
    if (output.results && output.results.message) {
        console.error('Message object:', output.results.message);
    }
    return 'Error: Could not extract message text. Check console for details.';
}

// Add message to chat
function addMessageToChat(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-fade-in flex ' + (type === 'user' ? 'justify-end' : 'justify-start');
    
    const bubble = document.createElement('div');
    bubble.className = `max-w-[85%] md:max-w-[70%] rounded-lg px-4 py-3 ${getMessageStyle(type)}`;
    
    // Format message content
    const content = document.createElement('div');
    
    // For AI messages, render markdown; for user/error, use plain text
    if (type === 'ai') {
        content.className = 'text-sm md:text-base break-words markdown-content';
        // Use marked.js to parse markdown
        content.innerHTML = marked.parse(message);
    } else {
        content.className = 'text-sm md:text-base break-words whitespace-pre-wrap';
        content.textContent = message;
    }
    
    // Add timestamp
    const timestamp = document.createElement('div');
    timestamp.className = 'text-xs mt-1 opacity-70';
    timestamp.textContent = new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    bubble.appendChild(content);
    bubble.appendChild(timestamp);
    messageDiv.appendChild(bubble);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
    
    // Store in history
    state.messageHistory.push({ message, type, timestamp: new Date() });
}

// Get message style based on type
function getMessageStyle(type) {
    switch (type) {
        case 'user':
            return 'bg-ibm-blue text-white ml-auto';
        case 'ai':
            return 'bg-gray-100 text-gray-800';
        case 'error':
            return 'bg-red-100 text-red-800 border border-red-300';
        default:
            return 'bg-gray-100 text-gray-800';
    }
}

// Show typing indicator
function showTypingIndicator() {
    const id = 'typing-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.id = id;
    messageDiv.className = 'message-fade-in flex justify-start';
    
    const bubble = document.createElement('div');
    bubble.className = 'bg-gray-100 rounded-lg px-4 py-3';
    
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'typing-indicator flex space-x-1';
    typingIndicator.innerHTML = `
        <span class="w-2 h-2 bg-gray-500 rounded-full"></span>
        <span class="w-2 h-2 bg-gray-500 rounded-full"></span>
        <span class="w-2 h-2 bg-gray-500 rounded-full"></span>
    `;
    
    bubble.appendChild(typingIndicator);
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
    
    return id;
}

// Remove typing indicator
function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

// Update send button state
function updateSendButton(disabled) {
    sendButton.disabled = disabled;
    if (disabled) {
        sendButton.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
        sendButton.classList.remove('opacity-50', 'cursor-not-allowed');
    }
}

// Update connection status
function updateConnectionStatus(connected) {
    if (connected) {
        connectionStatus.innerHTML = `
            <span class="w-2 h-2 md:w-3 md:h-3 bg-green-400 rounded-full mr-2 animate-pulse"></span>
            Connected
        `;
    } else {
        connectionStatus.innerHTML = `
            <span class="w-2 h-2 md:w-3 md:h-3 bg-red-400 rounded-full mr-2"></span>
            Disconnected
        `;
    }
}

// Auto-resize textarea
function autoResizeTextarea() {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
}

// Handle key press
function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatForm.dispatchEvent(new Event('submit'));
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send sample query (called from HTML buttons)
function sendSampleQuery(query) {
    userInput.value = query;
    userInput.focus();
    chatForm.dispatchEvent(new Event('submit'));
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        sendMessage,
        callLangflowAPI,
        extractMessageFromOutput
    };
}
