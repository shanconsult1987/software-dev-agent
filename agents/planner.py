
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SYSTEM_PROMPT = """
You are the Planner Agent in a software development factory.

Your responsibility is to analyse software requirements
and create an implementation plan.

Rules:
1. Do not write application code.
2. Do not execute commands.
3. Do not modify files.
4. Identify affected files.
5. Define implementation steps.
6. Define acceptance criteria.
7. Identify risks.
8. Return valid JSON only.

JSON structure:
{
  "objective": "",
  "affected_files": [],
  "steps": [],
  "acceptance_criteria": [],
  "risks": [],
  "requires_human_approval": true
}
"""


def create_plan(requirement):
    if not requirement or not requirement.strip():
        raise ValueError("Requirement cannot be empty")

    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"]
    )

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        instructions=SYSTEM_PROMPT,
        input=requirement
    )

    result = json.loads(response.output_text)

    required = {
        "objective",
        "affected_files",
        "steps",
        "acceptance_criteria",
        "risks",
        "requires_human_approval"
    }

    if not required.issubset(result):
        raise ValueError("Invalid planner output")

    return result


if __name__ == "__main__":
    requirement = (
        "Add low, medium and high priority "
        "to the task management application."
    )

    print(json.dumps(
        create_plan(requirement),
        indent=2
    ))
