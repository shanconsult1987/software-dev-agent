import json
from pathlib import Path
import shutil
import subprocess
import sys


def test_evaluator_sample_passes_all_checks(tmp_path):
    root = Path(__file__).resolve().parents[1]
    data = tmp_path / "data"
    data.mkdir()
    shutil.copyfile(root / "data" / "evaluation.json", data / "evaluation.json")

    result = subprocess.run(
        [sys.executable, str(root / "agents" / "evaluator.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["total"] > 0
    assert report["passed"] == report["total"]
    assert report["failed"] == 0
    assert report["pass_rate"] == 1.0
    assert all(item["passed"] for item in report["results"])
    assert json.loads(
        (data / "evaluation_report.json").read_text(encoding="utf-8")
    ) == report
