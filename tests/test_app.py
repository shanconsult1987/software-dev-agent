from app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.json["service"] == "Software Development Agent"


def test_projects():
    client = app.test_client()

    response = client.get("/projects")

    assert response.status_code == 200
    assert len(response.json) >= 1


def test_project_not_found():
    client = app.test_client()

    response = client.get("/projects/999")

    assert response.status_code == 404