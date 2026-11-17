import json
import os
from pathlib import Path

from agents.orchestrator import orchestrate


def get_github_event():

    event_path = os.getenv("GITHUB_EVENT_PATH")

    if not event_path:
        raise ValueError("GitHub event file not available")

    return json.loads(
        Path(event_path).read_text(encoding="utf-8")
    )


def main():

    event = get_github_event()

    issue = event.get("issue")

    if issue:

        issue_id = issue.get("number")

        title = issue.get("title", "")

        body = issue.get("body") or ""

        requirement = f"""
GitHub Issue: #{issue_id}

Title:
{title}

Description:
{body}
"""

    else:

        inputs = event.get("inputs", {})

        requirement = inputs.get("requirement", "")

        issue_id = None

    if not requirement.strip():
        raise ValueError("No requirement provided")

    print("Starting software development agents.")

    result = orchestrate(
        requirement=requirement,
        issue_id=issue_id
    )

    print("Agent execution completed.")

    print("Status:", result["status"])


if __name__ == "__main__":
    main()