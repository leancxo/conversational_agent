"""
DiaAgent implementation using the Dia framework for text-to-speech.
"""
import tempfile
import os
from pathlib import Path
import logging
from typing import Optional
from dia.model import Dia
import shutil

logger = logging.getLogger(__name__)

class DiaAgent:
    def __init__(self, compute_dtype: str = "float16"):
        """Initialize the Dia agent for text-to-speech generation.
        
        Args:
            compute_dtype: Computation data type ("float16", "float32", or "bfloat16")
        """
        self.model = None
        self.compute_dtype = compute_dtype
        self.temp_files = set()
        self.initialize_model()
        
    def initialize_model(self):
        """Initialize the Dia model."""
        try:
            self.model = Dia.from_pretrained(
                "nari-labs/Dia-1.6B",
                compute_dtype=self.compute_dtype
            )
            logger.info("Dia model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Dia model: {e}")
            raise
    
    def generate_speech(self, text: str, output_path: Optional[str] = None) -> str:
        """Generate speech from text using Dia.
        
        Args:
            text: Input text to convert to speech
            output_path: Optional path to save the audio file
            
        Returns:
            Path to the generated audio file
        """
        try:
            if not text.strip():
                raise ValueError("Input text cannot be empty")
                
            # Format text for dialogue generation
            formatted_text = f"[S1] {text}"
            
            # Generate audio (disabled torch compilation for Metal compatibility)
            audio_data = self.model.generate(
                formatted_text,
                use_torch_compile=False,  # Disabled for Metal compatibility
                verbose=True
            )
            
            # Save to temporary file if no output path specified
            if output_path is None:
                temp_dir = tempfile.gettempdir()
                output_path = os.path.join(temp_dir, f"dia_output_{hash(text)}.mp3")
                self.temp_files.add(output_path)
            
            # Save audio
            self.model.save_audio(output_path, audio_data)
            logger.info(f"Generated speech saved to {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Failed to generate speech: {e}")
            raise
    
    def process_message(self, message: str) -> str:
        """Process a message and return a response.
        
        Args:
            message: Input message from the user
            
        Returns:
            Response text
        """
        try:
            if not message.strip():
                return "I didn't receive any message. Please try again."
                
            # For now, just echo the message
            # In a real implementation, this would use a language model
            return f"I received your message: {message}"
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "Sorry, I encountered an error processing your message."
    
    def cleanup(self):
        """Clean up temporary files."""
        for file_path in self.temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                logger.error(f"Failed to remove temporary file {file_path}: {e}")
        self.temp_files.clear()
        
    def __del__(self):
        """Cleanup when the object is destroyed."""
        self.cleanup() 