
import json
from pathlib import Path

STATE_FILE = Path("data/agent_state.json")
MEMORY_FILE = Path("data/memory.json")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )
    temporary.replace(path)


def load_state():
    return load_json(STATE_FILE)


def save_state(state):
    save_json(STATE_FILE, state)


def update_state(**changes):
    state = load_state()
    state.update(changes)
    save_state(state)
    return state


def load_memory():
    return load_json(MEMORY_FILE)


def add_decision(decision, reason):
    memory = load_memory()

    memory["decisions"].append({
        "id": f"DEC-{len(memory['decisions']) + 1:03d}",
        "decision": decision,
        "reason": reason
    })

    save_json(MEMORY_FILE, memory)
    return memory


def get_context():
    return {
        "state": load_state(),
        "memory": load_memory()
    }


if __name__ == "__main__":
    print(json.dumps(get_context(), indent=2))
