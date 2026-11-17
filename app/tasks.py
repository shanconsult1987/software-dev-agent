
TASKS = [
    {
        "id": 1,
        "title": "Create login module",
        "priority": "high",
        "status": "open"
    },
    {
        "id": 2,
        "title": "Write unit tests",
        "priority": "medium",
        "status": "open"
    }
]

VALID_PRIORITIES = {"low", "medium", "high"}


def get_tasks():
    return TASKS


def get_task(task_id):
    for task in TASKS:
        if task["id"] == task_id:
            return task
    return None


def create_task(title, priority="medium"):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Task title is required")

    if priority not in VALID_PRIORITIES:
        raise ValueError("Invalid priority")

    task = {
        "id": max((t["id"] for t in TASKS), default=0) + 1,
        "title": title.strip(),
        "priority": priority,
        "status": "open"
    }

    TASKS.append(task)
    return task


def update_status(task_id, status):
    if status not in {"open", "in_progress", "completed"}:
        raise ValueError("Invalid status")

    task = get_task(task_id)

    if task is None:
        raise ValueError("Task not found")

    task["status"] = status
    return task
