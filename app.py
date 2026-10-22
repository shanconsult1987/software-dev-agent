from flask import Flask, jsonify
from pathlib import Path
from datetime import datetime, timezone
import json


app = Flask(__name__)


# ============================================================
# Agent state and audit configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
AGENT_DIR = BASE_DIR / ".agent"

STATE_FILE = AGENT_DIR / "state.json"
AUDIT_FILE = AGENT_DIR / "audit.jsonl"


# ============================================================
# Initial agent state
# ============================================================

DEFAULT_STATE = {
    "mission_id": "DEV-001",
    "status": "ready",
    "current_phase": "research",
    "completed_phases": [],
    "next_phase": "plan",
    "last_test_status": None,
    "last_evaluation": None
}


def ensure_agent_files():
    """
    Ensure the state and audit files exist.

    This gives the application a durable foundation
    for state tracking and auditability from the beginning.
    """

    AGENT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not STATE_FILE.exists():
        STATE_FILE.write_text(
            json.dumps(
                DEFAULT_STATE,
                indent=2
            ),
            encoding="utf-8"
        )

    if not AUDIT_FILE.exists():
        AUDIT_FILE.touch()


def load_state():
    ensure_agent_files()

    try:
        return json.loads(
            STATE_FILE.read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError:

        return DEFAULT_STATE.copy()


def save_state(state):
    ensure_agent_files()

    STATE_FILE.write_text(
        json.dumps(
            state,
            indent=2
        ),
        encoding="utf-8"
    )


def audit(event, details=None):
    """
    Append an immutable-style JSONL audit record.

    Each action gets:

    - timestamp
    - event
    - details
    """

    ensure_agent_files()

    record = {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "event": event,
        "details": details or {}
    }

    with AUDIT_FILE.open(
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(record) + "\n"
        )


# Initialize state/audit infrastructure
# immediately when the application starts.
ensure_agent_files()


# ============================================================
# CityOps incident data
# ============================================================

INCIDENTS = [
    {
        "id": 1,
        "title": "API unavailable",
        "severity": "high",
        "status": "open"
    },
    {
        "id": 2,
        "title": "Slow dashboard",
        "severity": "medium",
        "status": "open"
    }
]


# ============================================================
# Application endpoints
# ============================================================

@app.get("/")
def home():

    audit(
        "health_check",
        {
            "endpoint": "/"
        }
    )

    return jsonify({
        "service": "CityOps",
        "status": "healthy"
    })


@app.get("/incidents")
def get_incidents():

    audit(
        "list_incidents",
        {
            "count": len(INCIDENTS)
        }
    )

    return jsonify(INCIDENTS)


@app.get("/incidents/<int:incident_id>")
def get_incident(incident_id):

    incident = next(
        (
            item
            for item in INCIDENTS
            if item["id"] == incident_id
        ),
        None
    )

    if not incident:

        audit(
            "incident_not_found",
            {
                "incident_id": incident_id
            }
        )

        return jsonify({
            "error": "Incident not found"
        }), 404

    audit(
        "get_incident",
        {
            "incident_id": incident_id
        }
    )

    return jsonify(incident)


@app.get("/incidents/<int:incident_id>/priority")
def get_incident_priority(incident_id):

    incident = next(
        (
            item
            for item in INCIDENTS
            if item["id"] == incident_id
        ),
        None
    )

    if not incident:

        audit(
            "incident_not_found",
            {
                "incident_id": incident_id
            }
        )

        return jsonify({
            "error": "Incident not found"
        }), 404

    priority = {
        "high": "P1",
        "medium": "P2"
    }[incident["severity"]]

    audit(
        "get_incident_priority",
        {
            "incident_id": incident_id,
            "priority": priority
        }
    )

    return jsonify({
        "id": incident_id,
        "priority": priority
    })


# ============================================================
# Agent state endpoints
# ============================================================

@app.get("/agent/state")
def get_agent_state():

    state = load_state()

    audit(
        "read_agent_state",
        {
            "mission_id": state["mission_id"]
        }
    )

    return jsonify(state)


@app.get("/agent/audit")
def get_agent_audit():

    ensure_agent_files()

    records = []

    for line in AUDIT_FILE.read_text(
        encoding="utf-8"
    ).splitlines():

        if line.strip():
            records.append(
                json.loads(line)
            )

    return jsonify(records)


# ============================================================
# Application entry point
# ============================================================

if __name__ == "__main__":

    audit(
        "application_started",
        {
            "state_file": str(STATE_FILE),
            "audit_file": str(AUDIT_FILE)
        }
    )

    app.run(
        host="0.0.0.0",
        port=5000
    )