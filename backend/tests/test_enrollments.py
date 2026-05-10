from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_enroll_student_unauthorized():
    response = client.post("/enrollments/1")
    assert response.status_code in [401, 403]

def test_enroll_in_nonexistent_course_unauthorized():
    response = client.post("/enrollments/9999")
    assert response.status_code in [401, 403]


from routers.enrollments import get_current_user


class MockUser:
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role


def mock_get_current_user():
    return MockUser(id=1, username="test_user", role="student")


def test_enroll_student_success():
    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = client.post("/enrollments/1")

    app.dependency_overrides.clear()

    assert response.status_code in [200, 201]
    assert response.json()["message"] == "Enrollment successful"