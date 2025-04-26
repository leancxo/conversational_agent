import pytest
from fastapi.testclient import TestClient
from src.main import app
import os

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_websocket_connection():
    with client.websocket_connect("/ws") as websocket:
        # Send a test message
        websocket.send_json({"text": "Hello, this is a test."})
        
        # Receive the response
        response = websocket.receive_bytes()
        assert isinstance(response, bytes)
        assert len(response) > 0

def test_websocket_invalid_message():
    with client.websocket_connect("/ws") as websocket:
        # Send an invalid message
        websocket.send_json({"invalid": "message"})
        
        # Receive the error response
        response = websocket.receive_json()
        assert "error" in response
        assert "Missing 'text' field" in response["error"]

def test_static_files():
    # Test CSS file
    response = client.get("/static/css/styles.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]
    
    # Test JavaScript file
    response = client.get("/static/js/chat.js")
    assert response.status_code == 200
    assert "application/javascript" in response.headers["content-type"]

def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Conversational Agent" in response.text
    assert "chat-container" in response.text
    assert "text-input" in response.text 