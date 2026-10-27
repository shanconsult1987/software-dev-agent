from flask import Flask, jsonify, request

app = Flask(__name__)

PROJECTS = [
    {
        "id": 1,
        "name": "Payments API",
        "status": "active"
    },
    {
        "id": 2,
        "name": "Customer Portal",
        "status": "active"
    }
]


@app.get("/")
def home():
    return jsonify({
        "service": "Software Development Agent",
        "status": "running"
    })


@app.get("/projects")
def get_projects():
    return jsonify(PROJECTS)


@app.get("/projects/<int:project_id>")
def get_project(project_id):
    for project in PROJECTS:
        if project["id"] == project_id:
            return jsonify(project)

    return jsonify({"error": "Project not found"}), 404


@app.get("/projects/<int:project_id>/health")
def get_project_health(project_id):
    for project in PROJECTS:
        if project["id"] == project_id:
            return jsonify({
                "project_id": project["id"],
                "project_name": project["name"],
                "health_status": "healthy"
            })

    return jsonify({"error": "Project not found"}), 404


@app.get("/projects/<int:project_id>/status")
def get_project_status(project_id):
    for project in PROJECTS:
        if project["id"] == project_id:
            return jsonify({
                "id": project["id"],
                "name": project["name"],
                "status": project["status"]
            })

    return jsonify({"error": "Project not found"}), 404


@app.post("/projects")
def create_project():
    data = request.get_json()

    project = {
        "id": len(PROJECTS) + 1,
        "name": data["name"],
        "status": "active"
    }

    PROJECTS.append(project)

    return jsonify(project), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)