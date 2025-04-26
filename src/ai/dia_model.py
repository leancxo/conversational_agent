import os
from typing import Optional, List, Dict
import tempfile
import pyttsx3
import io
import logging
import time
import uuid
import random

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DiaAgent:
    def __init__(self, model_path: Optional[str] = None):
        """Initialize the voice agent."""
        logger.info("Initializing Voice Agent with pyttsx3")
        self.model_path = model_path or os.getenv("DIA_MODEL_PATH")
        self.conversation_history: List[Dict] = []
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Configure the voice
        voices = self.engine.getProperty('voices')
        # Try to set a female voice if available
        for voice in voices:
            if "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Set speech rate and volume
        self.engine.setProperty('rate', 175)  # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume level
        
        # Personality traits
        self.name = "Dia"
        self.personality = "helpful, friendly, and empathetic"
        
        # Response templates
        self.greetings = [
            f"Hi, I'm {self.name}, your voice assistant. How can I help you today?",
            f"Hello! This is {self.name}. What can I do for you?",
            f"Hey there! {self.name} here. Ready to assist you!",
            f"Greetings! I'm {self.name}, your AI assistant. How may I help?"
        ]
        
        self.acknowledgments = [
            "I understand.",
            "Got it.",
            "I see.",
            "Alright.",
        ]
        
        self.follow_ups = [
            "Is there anything specific you'd like to know?",
            "How can I assist you with that?",
            "Would you like me to explain further?",
            "What would you like me to help you with?",
        ]
        
        self.clarifications = [
            "Could you please elaborate on that?",
            "Would you mind providing more details?",
            "Could you tell me more about what you're looking for?",
            "I'd like to understand better what you need.",
        ]
        
        logger.info("Voice Agent initialized successfully")
    
    def process_message(self, text: str) -> str:
        """Process an incoming message and return a response."""
        logger.info(f"Processing message: {text[:50]}...")
        
        # Add message to conversation history
        self.conversation_history.append({"role": "user", "content": text})
        
        # Generate response based on context
        text_lower = text.lower()
        
        # Handle greetings
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            response = random.choice(self.greetings)
        
        # Handle questions about the agent
        elif any(word in text_lower for word in ['who are you', 'what are you', 'your name']):
            response = f"I'm {self.name}, an AI voice assistant. I'm here to help you with whatever you need."
        
        # Handle goodbyes
        elif any(word in text_lower for word in ['bye', 'goodbye', 'see you', 'farewell']):
            response = f"Goodbye! Feel free to talk to me anytime you need assistance."
        
        # Handle thank you
        elif any(word in text_lower for word in ['thank', 'thanks']):
            response = "You're welcome! Is there anything else I can help you with?"
        
        # Handle general queries
        else:
            # Combine acknowledgment with follow-up or clarification
            response = f"{random.choice(self.acknowledgments)} {random.choice(self.follow_ups if len(text.split()) > 5 else self.clarifications)}"
        
        # Add response to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        logger.info(f"Generated response: {response[:50]}...")
        return response
    
    def generate_speech(self, text: str) -> str:
        """Generate speech from text using pyttsx3 and save to a file."""
        try:
            logger.info(f"Starting speech generation for text: {text[:50]}...")
            start_time = time.time()
            
            # Create a unique filename
            filename = f"speech_{uuid.uuid4()}.mp3"
            temp_dir = tempfile.gettempdir()
            filepath = os.path.join(temp_dir, filename)
            
            logger.info(f"Will save audio to: {filepath}")
            
            # Generate speech using pyttsx3
            logger.info("Generating speech...")
            self.engine.save_to_file(text, filepath)
            self.engine.runAndWait()
            
            # Verify file exists and has content
            if not os.path.exists(filepath):
                raise RuntimeError("Audio file was not created")
            
            if os.path.getsize(filepath) == 0:
                raise RuntimeError("Audio file is empty")
            
            end_time = time.time()
            logger.info(f"Speech generation completed in {end_time - start_time:.2f} seconds")
            
            return filename
            
        except Exception as e:
            logger.error(f"Failed to generate speech: {str(e)}")
            logger.exception("Full traceback:")
            raise RuntimeError(f"Failed to generate speech: {str(e)}")
    
    def cleanup(self):
        """Clean up resources."""
        logger.info("Cleaning up Voice Agent resources")
        try:
            # Stop the TTS engine
            self.engine.stop()
        except:
            pass
            
        # Clean up any temporary audio files
        temp_dir = tempfile.gettempdir()
        for file in os.listdir(temp_dir):
            if file.startswith("speech_") and file.endswith(".mp3"):
                try:
                    filepath = os.path.join(temp_dir, file)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                        logger.info(f"Removed temporary file: {filepath}")
                except Exception as e:
                    logger.error(f"Failed to remove temporary file {file}: {e}")
        logger.info("Cleanup completed") 