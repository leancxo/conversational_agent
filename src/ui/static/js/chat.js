// WebSocket connection
let ws = null;
let isConnected = false;
let isTTSEnabled = true;

// DOM elements
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-btn');
const voiceInputButton = document.getElementById('voice-input-btn');
const ttsToggle = document.getElementById('tts-toggle');
const statusLight = document.getElementById('status-light');
const statusText = document.getElementById('status-text');

// Initialize WebSocket connection
function connect() {
    ws = new WebSocket(`ws://${window.location.host}/ws`);
    
    ws.onopen = () => {
        isConnected = true;
        updateStatus('Connected', 'connected');
    };
    
    ws.onmessage = (event) => {
        if (event.data instanceof Blob) {
            // Handle audio data
            if (isTTSEnabled) {
                const audio = new Audio(URL.createObjectURL(event.data));
                audio.play();
            }
        } else {
            // Handle text messages
            const message = JSON.parse(event.data);
            if (message.error) {
                addMessage(message.error, 'agent', true);
            }
        }
    };
    
    ws.onclose = () => {
        isConnected = false;
        updateStatus('Disconnected', 'disconnected');
        setTimeout(connect, 1000);
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        updateStatus('Error', 'error');
    };
}

// Update connection status
function updateStatus(text, className) {
    statusText.textContent = text;
    statusLight.className = `status-light ${className}`;
}

// Add message to chat
function addMessage(text, sender, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    if (isError) {
        messageDiv.style.color = 'red';
    }
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send message
function sendMessage() {
    const text = messageInput.value.trim();
    if (text && ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ text }));
        addMessage(text, 'user');
        messageInput.value = '';
    }
}

// Toggle TTS
function toggleTTS() {
    isTTSEnabled = !isTTSEnabled;
    ttsToggle.classList.toggle('active', isTTSEnabled);
}

// Voice input
let mediaRecorder = null;
let audioChunks = [];

async function startVoiceInput() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            // Here you would typically send the audio to a speech-to-text service
            // For now, we'll just show a placeholder message
            addMessage('Voice input received (STT not implemented)', 'user');
            audioChunks = [];
        };
        
        mediaRecorder.start();
        voiceInputButton.classList.add('recording');
    } catch (error) {
        console.error('Error accessing microphone:', error);
        addMessage('Error accessing microphone', 'agent', true);
    }
}

function stopVoiceInput() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        voiceInputButton.classList.remove('recording');
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

ttsToggle.addEventListener('click', toggleTTS);

voiceInputButton.addEventListener('mousedown', startVoiceInput);
voiceInputButton.addEventListener('mouseup', stopVoiceInput);
voiceInputButton.addEventListener('mouseleave', stopVoiceInput);

// Initialize
connect(); 