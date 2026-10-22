import json
import unittest
from unittest.mock import patch

from app import (
    app,
    INCIDENTS,
    STATE_FILE,
    AUDIT_FILE,
    ensure_agent_files
)


class TestCityOps(unittest.TestCase):

    def setUp(self):

        ensure_agent_files()

        self.client = app.test_client()

    def test_agent_files_exist(self):

        self.assertTrue(
            STATE_FILE.exists()
        )

        self.assertTrue(
            AUDIT_FILE.exists()
        )

    def test_home(self):

        response = self.client.get("/")

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json["status"],
            "healthy"
        )

    def test_get_incidents(self):

        response = self.client.get(
            "/incidents"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.json),
            2
        )

    def test_get_existing_incident(self):

        response = self.client.get(
            "/incidents/1"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json["severity"],
            "high"
        )

    def test_get_missing_incident(self):

        response = self.client.get(
            "/incidents/999"
        )

        self.assertEqual(
            response.status_code,
            404
        )

    def test_agent_state(self):

        response = self.client.get(
            "/agent/state"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            response.json["mission_id"],
            "DEV-001"
        )

    def test_get_incident_priority(self):

        for incident_id, priority in ((1, "P1"), (2, "P2")):
            with self.subTest(incident_id=incident_id):

                response = self.client.get(
                    f"/incidents/{incident_id}/priority"
                )

                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.is_json)
                self.assertEqual(
                    response.json,
                    {"id": incident_id, "priority": priority}
                )

                record = json.loads(
                    AUDIT_FILE.read_text(encoding="utf-8").splitlines()[-1]
                )
                self.assertEqual(record["event"], "get_incident_priority")
                self.assertEqual(
                    record["details"],
                    {"incident_id": incident_id, "priority": priority}
                )

    def test_closed_incident_priority(self):

        for severity, priority in (("high", "P1"), ("medium", "P2")):
            with self.subTest(severity=severity):
                with patch("app.INCIDENTS", [{
                    "id": 1,
                    "title": "Resolved incident",
                    "severity": severity,
                    "status": "closed"
                }]):

                    response = self.client.get("/incidents/1/priority")

                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(
                        response.json,
                        {"id": 1, "priority": priority}
                    )

    def test_get_missing_incident_priority(self):

        response = self.client.get("/incidents/999/priority")

        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.is_json)
        self.assertEqual(response.json, {"error": "Incident not found"})

        record = json.loads(
            AUDIT_FILE.read_text(encoding="utf-8").splitlines()[-1]
        )
        self.assertEqual(record["event"], "incident_not_found")
        self.assertEqual(record["details"], {"incident_id": 999})

    def test_priority_preserves_incident_responses(self):

        expected = [dict(incident) for incident in INCIDENTS]

        for incident in expected:
            self.client.get(f"/incidents/{incident['id']}/priority")
            response = self.client.get(f"/incidents/{incident['id']}")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, incident)

        response = self.client.get("/incidents")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected)
        self.assertEqual(INCIDENTS, expected)

    def test_audit_endpoint(self):

        self.client.get("/")

        response = self.client.get(
            "/agent/audit"
        )

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertGreater(
            len(response.json),
            0
        )


if __name__ == "__main__":
    unittest.main()