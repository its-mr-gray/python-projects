def list_all_tasks(
    data: dict[str, list[str]],
) -> dict[str, list[str]]:
    return data


def list_unfinished_tasks(
    data: dict[str, list[str]],
    task_status: list[str],
) -> list[str]:
    unfinished_tasks = []
    for val in task_status:
        for vals in data[val]:
            unfinished_tasks.append(vals)
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
    current_task_status: list[str],
    task: str,
    new_task_status: str,
) -> dict[str, list[str]]:
    pass


def remove_task(
    data: dict[str, list[str]],
    task: str,
    task_status: str,
) -> dict[str, list[str]]:
    data[task_status] = [val for val in data[task_status] if val != task]
    return data
