import json
import os
from typing import Any


def create_load_json(
    json_file: Any, default_data: dict[str, list[str]]
) -> dict[str, list[str]] | None:
    if not os.path.exists(json_file):
        with open(json_file, "w") as f:
            json.dump(default_data, f, indent=2)

    try:
        with open(json_file, "r") as f:
            data: dict = json.load(f)
            return data
    except json.JSONDecodeError:
        print("the .json file is corrupted.")
        return None


def write_to_json(data: dict[str, list[str]], file: Any) -> None:
    with open(file, "w") as f:
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()


def list_all_tasks(
    data: dict[str, list[str]],
) -> dict[str, list[str]]:
    return data


def list_unfinished_tasks(
    data: dict[str, list[str]],
    task_status: list[str],
) -> list[str]:
    for status in task_status:
        unfinished_tasks = [tasks for tasks in data[status]]

    return unfinished_tasks


def list_tasks_by_status(
    data: dict[str, list[str]],
    task_status: str,
) -> list[str]:
    return data[task_status]


def add_task(
    data: dict[str, list[str]],
    task_status: str,
    task: str,
    file: Any,
) -> list[str]:
    data[task_status].append(task)
    write_to_json(data=data, file=file)

    return data[task_status]


def update_task_status(
    data: dict[str, list[str]],
    task: str,
    current_status: str,
    new_task_status: str,
    file: Any,
) -> dict[str, list[str]]:
    data[current_status].remove(task)
    data[new_task_status].append(task)
    write_to_json(data=data, file=file)

    return data


def remove_task(
    data: dict[str, list[str]],
    task: str,
    task_status: str,
    file: Any,
) -> dict[str, list[str]]:
    data[task_status] = [val for val in data[task_status] if val != task]
    write_to_json(data=data, file=file)
    return data
