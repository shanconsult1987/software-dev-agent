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


def test_project_health():
    client = app.test_client()

    response = client.get("/projects/1/health")

    assert response.status_code == 200
    assert response.json["project_id"] == 1
    assert response.json["project_name"] == "Payments API"
    assert response.json["health_status"] == "healthy"


def test_project_health_not_found():
    client = app.test_client()

    response = client.get("/projects/999/health")

    assert response.status_code == 404