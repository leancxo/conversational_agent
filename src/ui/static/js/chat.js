class ChatApp {
    constructor() {
        this.messageInput = document.getElementById('message-input');
        this.sendButton = document.getElementById('send-btn');
        this.voiceButton = document.getElementById('voice-input-btn');
        this.chatMessages = document.getElementById('chat-messages');
        this.statusText = document.getElementById('status-text');
        this.statusLight = document.getElementById('status-light');
        
        this.ws = null;
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isAutoSending = false;
        this.audioPlayer = new Audio();
        
        this.initializeWebSocket();
        this.initializeSpeechRecognition();
        this.setupEventListeners();
    }
    
    initializeWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            this.updateConnectionStatus(true);
        };
        
        this.ws.onclose = () => {
            this.updateConnectionStatus(false);
            setTimeout(() => this.initializeWebSocket(), 3000);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus(false);
        };
        
        this.ws.onmessage = async (event) => {
            try {
                const response = JSON.parse(event.data);
                this.addMessage(response.text, 'agent');
                
                if (response.audio_path) {
                    const audioUrl = `/audio/${response.audio_path.split('/').pop()}`;
                    this.audioPlayer.src = audioUrl;
                    await this.audioPlayer.play();
                }
            } catch (error) {
                console.error('Error processing message:', error);
            }
        };
    }
    
    initializeSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            
            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                this.messageInput.value = transcript;
                if (this.isAutoSending) {
                    this.sendMessage();
                }
            };
            
            this.recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                this.voiceButton.classList.remove('recording');
                this.isAutoSending = false;
            };
            
            this.recognition.onend = () => {
                this.voiceButton.classList.remove('recording');
                this.isAutoSending = false;
            };
        } else {
            this.voiceButton.style.display = 'none';
            console.warn('Speech recognition not supported');
        }
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        this.messageInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                this.sendMessage();
            }
        });
        
        this.voiceButton.addEventListener('click', () => this.toggleVoiceInput());
        
        this.audioPlayer.addEventListener('play', () => {
            this.updateAgentStatus('Speaking');
        });
        
        this.audioPlayer.addEventListener('ended', () => {
            this.updateAgentStatus('Connected');
        });
        
        this.audioPlayer.addEventListener('error', (e) => {
            console.error('Audio playback error:', e);
            this.updateAgentStatus('Connected');
        });
    }
    
    sendMessage() {
        const message = this.messageInput.value.trim();
        if (message && this.ws.readyState === WebSocket.OPEN) {
            this.addMessage(message, 'user');
            
            const data = {
                text: message,
                require_audio: true
            };
            this.ws.send(JSON.stringify(data));
            
            this.messageInput.value = '';
            this.updateAgentStatus('Processing');
        }
    }
    
    addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.textContent = message;
        
        this.chatMessages.appendChild(messageElement);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    toggleVoiceInput() {
        if (!this.recognition) return;
        
        if (this.voiceButton.classList.contains('recording')) {
            this.recognition.stop();
        } else {
            if (this.synthesis) {
                this.synthesis.cancel();
            }
            if (this.audioPlayer) {
                this.audioPlayer.pause();
            }
            this.recognition.start();
            this.voiceButton.classList.add('recording');
            this.isAutoSending = true;
        }
    }
    
    updateConnectionStatus(connected) {
        this.statusText.textContent = connected ? 'Connected' : 'Disconnected';
        this.statusLight.classList.toggle('connected', connected);
        this.sendButton.disabled = !connected;
    }
    
    updateAgentStatus(status) {
        this.statusText.textContent = status;
        this.statusLight.classList.toggle('processing', status === 'Processing');
        this.statusLight.classList.toggle('speaking', status === 'Speaking');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
}); 