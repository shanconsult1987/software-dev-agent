# CityOps Software Development Agent

A minimal repository demonstrating an agentic
software development workflow using GitHub.

## Application

CityOps currently provides:

- health check
- incident listing
- incident retrieval
- incident priority
- agent state
- agent audit history

### Incident priority

`GET /incidents/<id>/priority` returns JSON with the incident ID and
priority, for example `{"id": 1, "priority": "P1"}`.
High severity maps to `P1` and medium severity maps to `P2`,
regardless of whether the incident is open or closed.
Missing incidents return HTTP 404 with
`{"error": "Incident not found"}`.
Existing incident listing and retrieval responses are unchanged.

## Agent architecture

The repository demonstrates:

- GitHub Issues
- repository instructions
- path-specific instructions
- custom agents
- skills
- prompts
- MCP
- state
- audit trail
- evaluation
- GitHub Actions
- security review
- hooks
- CODEOWNERS
- issue templates
- pull request templates
- human approval

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py