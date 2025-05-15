"""
The application should run from the command line, accept user actions and inputs as arguments, and store the tasks in a JSON file. The user should be able to:

    Add, Update, and Delete tasks
    Mark a task as in progress or done
    List all tasks <- DONE
    List all tasks that are done
    List all tasks that are not done
    List all tasks that are in progress

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
default_data = {"TODO": [], "IN PROGRESS": [], "DONE": []}

if not os.path.exists(json_file):
    with open(json_file, "w") as f:
        json.dump(default_data, f, indent=2)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True)
list_task_parser = subparsers.add_parser("list", help="list all tasks in the tracker.")
add_task_parser = subparsers.add_parser("add", help="add a new task.")
update_task_parser = subparsers.add_parser("update", help="update a task.")
remove_task_parser = subparsers.add_parser("remove", help="remove a task.")
args = parser.parse_args()

with open(json_file, "r+") as f:
    data = json.load(f)

    if args.command == "list":
        print(json.dumps(data, indent=2))
    elif args.command == "add":
        new_task = input("what would you like to add?")
        data["TODO"].append(new_task)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    elif args.command == "update":
        update_task = input("what task needs updating?")
        status_query = input(
            "does the status of this task need to be updated? Y/N \n"
        ).upper()
        if status_query == "Y":
            update_status = input("what is the updated status of this task?")
            # update status logic
        elif status_query == "N":
            updated_task = input("please input the update for this task")
            # update task logic
    elif args.command == "remove":
        remove_task = input("which task would you like to remove?")
        data["TODO"] = [task for task in data["TODO"] if task != remove_task]
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
