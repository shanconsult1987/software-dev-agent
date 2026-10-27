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