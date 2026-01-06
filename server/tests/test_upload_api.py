from fastapi.testclient import TestClient
from server.app import app

client = TestClient(app)

def test_upload_new_file(tmp_path):
    r = client.post(
        "/upload",
        files={"file": ("a.txt", b"hello")}
    )
    assert r.status_code == 200
    assert r.json()["message"] == "File uploaded successfully"


def test_upload_same_content_twice():
    client.post("/upload", files={"file": ("a.txt", b"hello")})
    r = client.post("/upload", files={"file": ("b.txt", b"hello")})

    assert "already exists" in r.json()["message"]
