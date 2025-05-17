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

from typing import Any

import utilities
from parsers import parser

json_file: Any = "tasklist.json"
default_data: dict[str, list[str]] = {
    "TODO": [],
    "IN PROGRESS": [],
    "DONE": [],
}
to_do_status: str = "TODO"
in_prog_status: str = "IN PROGRESS"
done_status: str = "DONE"

if __name__ == "__main__":
    args = parser.parse_args()

    data = utilities.create_load_json(json_file=json_file, default_data=default_data)

    if data is not None:
        if args.command == "list-all":
            all_tasks = utilities.list_all_tasks(data=data)
            print(all_tasks)
        elif args.command == "list-unfinished":
            incomplete_tasks = utilities.list_unfinished_tasks(
                data=data, task_status=[to_do_status, in_prog_status]
            )
            print(incomplete_tasks)
        elif args.command == "list-in-progress":
            in_progress_tasks = utilities.list_tasks_by_status(
                data=data, task_status=in_prog_status
            )
            print(in_progress_tasks)
        elif args.command == "list-done":
            done_tasks = utilities.list_tasks_by_status(
                data=data, task_status=done_status
            )
            print(done_tasks)
        elif args.command == "add":
            utilities.add_task(
                data=data,
                task_status=to_do_status,
                task=args.task,
                file=json_file,
            )
            print(data)
        elif args.command == "update-status":
            utilities.update_task_status(
                data=data,
                task=args.task,
                current_status=args.current_status,
                new_task_status=args.new_status,
                file=json_file,
            )
            print(data)
        elif args.command == "remove":
            utilities.remove_task(
                data=data,
                task=args.task,
                task_status=args.current_status,
                file=json_file,
            )
            print(data)
        else:
            print("invalid command. please type -h for list of commands.")
