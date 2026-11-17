
import pytest

from app.tasks import (
    create_task,
    get_task,
    get_tasks,
    update_status
)


def test_get_tasks():
    assert len(get_tasks()) >= 2


@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_create_task(priority):
    task = create_task("Build API", priority)

    assert task["title"] == "Build API"
    assert task["priority"] == priority


@pytest.mark.parametrize("priority", ["urgent", None, [], {}, 1])
def test_invalid_priority(priority):
    with pytest.raises(ValueError):
        create_task("Invalid task", priority)


def test_update_status():
    task = create_task("Write documentation")

    updated = update_status(task["id"], "completed")

    assert updated["status"] == "completed"


def test_invalid_status():
    task = create_task("Write tests")

    with pytest.raises(ValueError):
        update_status(task["id"], "unknown")


def test_missing_task():
    with pytest.raises(ValueError):
        update_status(99999, "completed")
