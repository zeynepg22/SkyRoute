from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_courses():
    response = client.get("/courses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_nonexistent_course():
    response = client.get("/courses/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"