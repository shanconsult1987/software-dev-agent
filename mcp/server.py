from pathlib import Path
import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("software-dev-agent")

ROOT = Path(__file__).resolve().parent.parent


@mcp.tool()
def get_project_info() -> str:
    """Return basic information about the software project."""

    return """
Software Development Agent Demo

Language: Python
Framework: Flask
Testing: pytest

Goal:
Use an AI agent to safely implement software changes.

Workflow:
Issue → Code → Test → Pull Request → CI → Deploy
"""


@mcp.tool()
def read_file(filename: str) -> str:
    """Read a file from the project."""

    file_path = ROOT / filename

    if not file_path.exists():
        return f"File not found: {filename}"

    return file_path.read_text(encoding="utf-8")


@mcp.tool()
def run_tests() -> str:
    """Run the project's pytest tests."""

    result = subprocess.run(
        ["python", "-m", "pytest", "-v"],
        cwd=ROOT,
        capture_output=True,
        text=True
    )

    return result.stdout + result.stderr


if __name__ == "__main__":
    mcp.run()