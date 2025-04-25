def test_index_page(client):
    """Test the main page loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
    # Check for important UI elements in the HTML
    content = response.text
    assert "<title>Conversational Agent</title>" in content
    assert 'id="chat-container"' in content
    assert 'id="message-input"' in content
    assert 'id="send-btn"' in content

def test_static_files(client):
    """Test that static files (CSS, JS) are accessible."""
    css_response = client.get("/static/css/styles.css")
    assert css_response.status_code == 200
    assert "text/css" in css_response.headers["content-type"]
    
    js_response = client.get("/static/js/chat.js")
    assert js_response.status_code == 200
    assert "text/javascript" in js_response.headers["content-type"] 