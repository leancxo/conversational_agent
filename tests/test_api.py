from fastapi.testclient import TestClient

def test_websocket_endpoint(client):
    """Test the WebSocket connection endpoint."""
    with client.websocket_connect("/ws") as websocket:
        # Send a test message
        test_data = {"text": "Hello", "require_audio": False}
        websocket.send_json(test_data)
        # Receive response
        response = websocket.receive_json()
        assert "text" in response
        assert response["text"] == "Echo: Hello"

def test_chat_health(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_send_message(client, test_message):
    """Test sending a message through the API."""
    response = client.post("/chat", json=test_message)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data 