
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from agents.state import update_state

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


AGENTS = {
    "planner": """
    You are the Planner Agent.
    Analyse the requirement.
    Create a structured implementation plan.
    Identify affected files, acceptance criteria and risks.
    Do not write code.
    """,

    "developer": """
    You are the Developer Agent.
    Analyse the approved plan.
    Propose implementation steps and test cases.
    Do not claim that files have been modified.
    Do not bypass approval.
    """,

    "reviewer": """
    You are the Reviewer Agent.
    Independently review the plan and developer proposal.
    Identify security risks, missing tests and conflicts.
    Return APPROVE or REJECT with reasons.
    Never approve an unsafe or incomplete change.
    """,

    "summary": """
    You are the Summary Agent.
    Summarise the work of the other agents.
    Record decisions, risks, review results and next steps.
    Distinguish proposed work from executed work.
    """
}


def run_agent(name, task):
    response = client.responses.create(
        model=MODEL,
        instructions=AGENTS[name],
        input=task
    )

    return response.output_text


def orchestrate(requirement):
    update_state(
        task=requirement,
        status="running",
        current_agent="planner",
        completed_agents=[],
        last_checkpoint="orchestration_started"
    )

    outputs = {}

    for name in ["planner", "developer", "reviewer", "summary"]:
        update_state(
            current_agent=name,
            last_checkpoint=f"{name}_started"
        )

        previous = json.dumps(outputs, indent=2)

        task = f"""
        Original requirement:
        {requirement}

        Previous agent outputs:
        {previous}

        Complete your assigned role.
        """

        try:
            outputs[name] = run_agent(name, task)

        except Exception as error:
            update_state(
                status="failed",
                last_checkpoint=f"{name}_failed"
            )
            raise RuntimeError(
                f"{name} agent failed: {error}"
            ) from error

        state = update_state(
            completed_agents=list(outputs.keys()),
            last_checkpoint=f"{name}_completed"
        )

    result = {
        "requirement": requirement,
        "agents": outputs
    }

    with open(
        "data/multi_agent_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(result, file, indent=2)

    update_state(
        status="completed",
        current_agent=None,
        last_checkpoint="orchestration_completed"
    )

    return result


if __name__ == "__main__":
    result = orchestrate(
        "Add low, medium and high priority "
        "to the task application."
    )

    print(json.dumps(result, indent=2))
