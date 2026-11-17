import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


@pytest.mark.parametrize("status", ["idle", "in_progress"])
def test_resume_script_without_pythonpath(tmp_path, status):
    data = tmp_path / "data"
    data.mkdir()
    state = {
        "status": status,
        "issue_id": 1,
        "task": "Example task",
        "current_agent": "developer",
        "last_checkpoint": "plan_approved",
    }
    (data / "agent_state.json").write_text(json.dumps(state), encoding="utf-8")
    (data / "memory.json").write_text(
        json.dumps({"decisions": [{"decision": "Follow approved plan"}]}),
        encoding="utf-8",
    )
    script = Path(__file__).resolve().parents[1] / "scripts" / "resume-agent.py"
    env = {
        key: value for key, value in os.environ.items()
        if key.upper() != "PYTHONPATH"
    }

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr
    if status == "idle":
        assert result.stdout == "No active execution to resume.\n"
    else:
        assert "Resuming agent execution" in result.stdout
        assert "Issue: 1" in result.stdout
        assert "Task: Example task" in result.stdout
        assert "Previous agent: developer" in result.stdout
        assert "Last checkpoint: plan_approved" in result.stdout
        assert "- Follow approved plan" in result.stdout
