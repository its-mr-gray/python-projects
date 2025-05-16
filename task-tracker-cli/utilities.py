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
) -> list[str]:
    data[task_status].append(task)

    return data[task_status]


def update_task_status(
    data: dict[str, list[str]],
    task: str,
    current_status: str,
    new_task_status: str,
) -> dict[str, list[str]]:
    data[current_status].remove(task)
    data[new_task_status].append(task)

    return data


def remove_task(
    data: dict[str, list[str]],
    task: str,
    task_status: str,
) -> dict[str, list[str]]:
    data[task_status] = [val for val in data[task_status] if val != task]

    return data
