import pytest
from src.ai.dia_model import DiaAgent
import os
import tempfile

def test_tts_generation():
    """Test that text-to-speech generation works."""
    agent = DiaAgent()
    
    # Test with a short text
    test_text = "Hello, this is a test of the text to speech system."
    filename = agent.generate_speech(test_text)
    
    # Verify we got a filename back
    assert isinstance(filename, str)
    assert filename.endswith('.mp3')
    
    # Check that the file exists
    filepath = os.path.join(tempfile.gettempdir(), filename)
    assert os.path.exists(filepath)
    
    # Clean up
    agent.cleanup()
    if os.path.exists(filepath):
        os.remove(filepath)

def test_message_processing():
    """Test that message processing works."""
    agent = DiaAgent()
    
    # Test with a sample message
    test_message = "Hello, how are you?"
    response = agent.process_message(test_message)
    
    # Verify we got a response
    assert isinstance(response, str)
    assert len(response) > 0
    assert "you said" in response.lower()

if __name__ == "__main__":
    # Run the tests directly
    test_tts_generation()
    test_message_processing()
    print("Tests completed successfully!") 