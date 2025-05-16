import argparse

parser: argparse.ArgumentParser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(
    title="task manipulation commands",
    description="various different operations to be performed on the task tracker",
    dest="command",
    required=True,
)

list_all_tasks_parser = subparsers.add_parser(
    "list-all", help="list all tasks in the tracker."
)
list_unfinished_tasks_parser = subparsers.add_parser(
    "list-unfinished", help="list all unfinished tasks in the tracker."
)
list_inprog_tasks_parser = subparsers.add_parser(
    "list-in-progress", help="list all in progress tasks in the tracker."
)
list_finished_tasks_parser = subparsers.add_parser(
    "list-done", help="list all finished tasks in the tracker."
)

add_task_parser = subparsers.add_parser("add", help="add a new task.")
add_task_parser.add_argument(
    "task",
    type=str,
    help="enter the task to be added. it will immediately be placed in TODO.",
)

update_task_parser = subparsers.add_parser(
    "update-status", help="update a task's status."
)
update_task_parser.add_argument(
    "task", type=str, help="enter the task that needs a status change."
)
update_task_parser.add_argument(
    "current_status",
    type=str,
    help="enter the current status of the task. this can be determined by running the 'list-all' command prior to updating.",
)
update_task_parser.add_argument(
    "new_status",
    type=str,
    help="enter the new status of a task. status options can be determined by running the 'list-all' command prior to updating.",
)

remove_task_parser = subparsers.add_parser("remove", help="remove a task.")
remove_task_parser.add_argument(
    "task",
    type=str,
    help="enter task to be removed. current tasks and statuses can be determined by running the 'list-all' command prior to removal.",
)
remove_task_parser.add_argument(
    "current_status",
    type=str,
    help="enter the current status of the task. this can be determined by running the 'list-all' command prior to removal.",
)
