import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Conversational Agent" in response.text
    assert "chat-container" in response.text
    assert "text-input" in response.text

def test_static_files():
    # Test CSS file
    response = client.get("/static/css/styles.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]
    
    # Test JavaScript file
    response = client.get("/static/js/chat.js")
    assert response.status_code == 200
    assert "application/javascript" in response.headers["content-type"] 