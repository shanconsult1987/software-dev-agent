import json
import subprocess
import sys


def run_tests():

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-v"
        ],
        capture_output=True,
        text=True
    )

    return {
        "passed": result.returncode == 0,
        "output": (
            result.stdout +
            result.stderr
        )
    }


def evaluate():

    result = run_tests()

    evaluation = {
        "tests_passed": result["passed"],
        "quality_gate": result["passed"],
        "recommendation": (
            "APPROVE"
            if result["passed"]
            else "REJECT"
        )
    }

    print(
        json.dumps(
            evaluation,
            indent=2
        )
    )

    return (
        0
        if result["passed"]
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(
        evaluate()
    )