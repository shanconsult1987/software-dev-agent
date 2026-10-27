import subprocess
import sys
from pathlib import Path

EVALUATE_SCRIPT = Path(__file__).resolve().parents[1] / "evals" / "evaluate.py"


def test_evaluate_passes_when_run_from_another_directory(tmp_path):
    result = subprocess.run(
        [sys.executable, str(EVALUATE_SCRIPT)],
        cwd=tmp_path,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "EVALUATION: PASS" in result.stdout
