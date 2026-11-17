
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents.state import get_context


def resume():
    context = get_context()
    state = context["state"]

    if state["status"] == "idle":
        print("No active execution to resume.")
        return

    print("Resuming agent execution")
    print("Issue:", state["issue_id"])
    print("Task:", state["task"])
    print("Previous agent:", state["current_agent"])
    print("Last checkpoint:", state["last_checkpoint"])

    print("\nPrevious decisions:")

    for decision in context["memory"]["decisions"]:
        print("-", decision["decision"])


if __name__ == "__main__":
    resume()
