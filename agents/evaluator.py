
import json
from pathlib import Path


DATASET = Path("data/evaluation.json")
REPORT = Path("data/evaluation_report.json")


def evaluate_output(requirement, output, expected_terms):
    normalized = output.lower()

    missing = [
        term for term in expected_terms
        if term.lower() not in normalized
    ]

    passed = len(missing) == 0

    return {
        "requirement": requirement,
        "passed": passed,
        "missing_terms": missing,
        "score": (
            len(expected_terms) - len(missing)
        ) / len(expected_terms)
    }


def run_evaluation(output_text):
    dataset = json.loads(
        DATASET.read_text(encoding="utf-8")
    )

    results = []

    for test in dataset["tests"]:
        result = evaluate_output(
            test["requirement"],
            output_text,
            test["expected_terms"]
        )

        result["test_id"] = test["id"]
        results.append(result)

    passed = sum(
        1 for item in results if item["passed"]
    )

    report = {
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": passed / len(results),
        "results": results
    }

    REPORT.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8"
    )

    return report


if __name__ == "__main__":
    sample = """
    The implementation adds priority validation.
    Supported values are low, medium and high.
    Invalid priority values return an error.
    Task status validation rejects invalid values
    with an error.
    The existing JSON and in-memory architecture
    is retained.
    """

    print(json.dumps(
        run_evaluation(sample),
        indent=2
    ))
