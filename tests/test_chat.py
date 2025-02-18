from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_response():
    """Test chatbot API response"""
    response = client.post("/chat", json={"user_input": "Hello", "thread_id": "123"})

    assert response.status_code == 200

    json_response = response.json()
    assert "messages" in json_response
    assert isinstance(json_response["messages"], list)
    assert len(json_response["messages"]) > 0
