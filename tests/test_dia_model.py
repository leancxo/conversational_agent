import pytest
from src.ai.dia_model import DiaAgent
import os

@pytest.fixture
def dia_agent():
    model_path = os.getenv("DIA_MODEL_PATH")
    if not model_path:
        pytest.skip("DIA_MODEL_PATH environment variable not set")
    return DiaAgent(model_path)

def test_dia_agent_initialization(dia_agent):
    assert dia_agent is not None
    assert dia_agent.model is not None
    assert dia_agent.device is not None

def test_generate_speech(dia_agent):
    text = "Hello, this is a test."
    audio_data = dia_agent.generate_speech(text)
    assert isinstance(audio_data, bytes)
    assert len(audio_data) > 0

def test_cleanup(dia_agent):
    dia_agent.cleanup()
    assert not hasattr(dia_agent, 'model') 