
from mcp.server.fastmcp import FastMCP

from app.tasks import get_task, get_tasks

mcp = FastMCP("Software Agent Development Tools")


@mcp.tool()
def list_tasks() -> list:
    """Return all available software tasks."""
    return get_tasks()


@mcp.tool()
def get_task_details(task_id: int) -> dict:
    """Retrieve a task using its ID."""

    task = get_task(task_id)

    if task is None:
        return {"error": "Task not found"}

    return task


@mcp.tool()
def validate_plan(
    objective: str,
    acceptance_criteria: list
) -> dict:
    """Validate whether a development plan has required fields."""

    errors = []

    if not objective.strip():
        errors.append("Objective is missing")

    if not acceptance_criteria:
        errors.append("Acceptance criteria are missing")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


if __name__ == "__main__":
    mcp.run()
