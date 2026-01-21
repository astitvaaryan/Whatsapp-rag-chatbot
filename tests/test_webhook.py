from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_webhook_get():
    # Twilio sends a GET request to verify webhook sometimes, or we just test endpoint existence
    # Note: Our webhook is POST, so GET might return 405 Method Not Allowed which confirms existence
    response = client.get("/whatsapp/webhook")
    assert response.status_code == 405

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]
