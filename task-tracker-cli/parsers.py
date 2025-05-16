import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True)
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
update_task_parser = subparsers.add_parser(
    "update-status", help="update a task's status."
)
remove_task_parser = subparsers.add_parser("remove", help="remove a task.")
args = parser.parse_args()
