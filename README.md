
# Software Development Agent

A small Python application used to demonstrate
agentic software development with GitHub.

## Features

- Task creation
- Task retrieval
- Task status updates
- Priority validation
- Automated tests

## Run

Install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run tests:

```powershell
python -m pytest -v
```

CI runs `python -m agents.evaluator` as its final step after the tests pass.
The evaluator prints a report and writes `data/evaluation_report.json`;
failed evaluation checks do not currently fail CI.

Resume agent execution from the repository root:

```powershell
python .\scripts\resume-agent.py
```

The script imports the repository's `agents` package directly and reads
`data/agent_state.json` and `data/memory.json` relative to the working directory.

## MCP server

Start `software-dev-tools` using the VS Code MCP configuration in
[.vscode/mcp.json](.vscode/mcp.json). It sets `PYTHONPATH` to the workspace root
so the server can import `app` when launched as a script.

The server provides `list_tasks`, `get_task_details`, and `validate_plan`.
After changing the configuration, restart the MCP server in VS Code.

## Architecture

The repository will progressively introduce:

- AI planning
- Custom agents
- MCP tools
- Agent state and memory
- Evaluation
- Multi-agent orchestration
- Guardrails and governance
- GitHub Actions automation
