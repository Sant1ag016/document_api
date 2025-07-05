""" from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_document():
    response = client.post("/upload", json={"document": "<mock_base64_string>"})
    assert response.status_code == 200
    assert "document_type" in response.json()
 """