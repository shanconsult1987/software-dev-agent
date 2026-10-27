import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_tests():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-v",
            "tests/test_app.py"
        ],
        capture_output=True,
        text=True,
        # Relative test path, so run pytest from the repo root.
        cwd=REPO_ROOT
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)

    return result.returncode == 0


def main():

    print("================================")
    print("Software Development Agent Eval")
    print("================================")

    if run_tests():
        print("EVALUATION: PASS")
        return 0

    print("EVALUATION: FAIL")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())