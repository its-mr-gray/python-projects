"""
The application should run from the command line, accept user actions and inputs as arguments, and store the tasks in a JSON file. The user should be able to:

    Add, Update, and Delete tasks <- DONE
    Mark a task as in progress or done <- DONE
    List all tasks <- DONE
    List all tasks that are done <- DONE
    List all tasks that are not done <- DONE
    List all tasks that are in progress <- DONE

Here are some constraints to guide the implementation:

    Use positional arguments in command line to accept user inputs. <- DONE
    Use a JSON file to store the tasks in the current directory. <- DONE
    The JSON file should be created if it does not exist. <- DONE
    Use the native file system module of your programming language to interact with the JSON file. <- Done
    Do not use any external libraries or frameworks to build this project. <- DONE
    Ensure to handle errors and edge cases gracefully.

"""

import argparse
import json
import os

json_file = "tasklist.json"
default_data: dict = {"TODO": [], "IN PROGRESS": [], "DONE": []}

if not os.path.exists(json_file):
    with open(json_file, "w") as f:
        json.dump(default_data, f, indent=2)

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

with open(json_file, "r+") as f:
    data = json.load(f)

    if args.command == "list-all":
        print(json.dumps(data, indent=2))

    elif args.command == "list-unfinished":
        todo_vals = [v for v in data["TODO"]]
        in_prog_vals = [v for v in data["IN PROGRESS"]]
        print(todo_vals + in_prog_vals)

    elif args.command == "list-done":
        print(json.dumps(data["DONE"], indent=2))

    elif args.command == "list-in-progress":
        print(json.dumps(data["IN PROGRESS"], indent=2))

    elif args.command == "add":
        new_task = input("what would you like to add?\n").upper()
        data["TODO"].append(new_task)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

    elif args.command == "update-status":
        todo_contents = [task for task in data["TODO"]]
        in_prog_contents = [task for task in data["IN PROGRESS"]]
        done_contents = [task for task in data["DONE"]]
        task_to_update = input(
            f"what task would you like to change the status of?\n {data.values()}"
        ).upper()
        if task_to_update in todo_contents:
            todo_contents.remove(task_to_update)
        elif task_to_update in in_prog_contents:
            in_prog_contents.remove(task_to_update)
        elif task_to_update in done_contents:
            done_contents.remove(task_to_update)
        status_to_update = input(
            f"what status should this task now have?\n{data.keys()}"
        ).upper()

        if status_to_update == "TODO":
            todo_contents.append(task_to_update)
        elif status_to_update == "IN PROGRESS":
            in_prog_contents.append(task_to_update)
        elif status_to_update == "DONE":
            done_contents.append(task_to_update)
        else:
            print("invalid status selection")

        data["TODO"] = list(todo_contents)
        data["IN PROGRESS"] = list(in_prog_contents)
        data["DONE"] = list(done_contents)
        if status_to_update not in data.keys():
            print("invalid status selection")
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()

    elif args.command == "remove":
        remove_task = input("which task would you like to remove?\n").upper()
        data["TODO"] = [task for task in data["TODO"] if task != remove_task]
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
