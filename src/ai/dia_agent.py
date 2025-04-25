"""
Mock DiaAgent for testing the chat interface.
"""
import tempfile
import os
from pathlib import Path

class DiaAgent:
    """A mock implementation of the Dia conversational agent."""
    
    def __init__(self):
        """Initialize the mock agent."""
        self.temp_dir = Path(tempfile.gettempdir())
    
    def generate_speech(self, text: str) -> str:
        """Mock speech generation - just returns a dummy file path."""
        # In a real implementation, this would generate actual audio
        dummy_file = self.temp_dir / "dummy_audio.mp3"
        return str(dummy_file)
    
    def process_message(self, message: str) -> str:
        """Process a message and return a response."""
        return f"I received your message: {message}" 