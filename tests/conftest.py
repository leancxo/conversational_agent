import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def test_message():
    """Sample message for testing."""
    return {"message": "Hello, this is a test message"} 