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

import json
import os
from typing import Any

json_file: Any = "tasklist.json"
default_data: dict = {"TODO": [], "IN PROGRESS": [], "DONE": []}

if not os.path.exists(json_file):
    with open(json_file, "w+") as f:
        json.dump(default_data, f, indent=2)

with open(json_file, "r") as f:
    data: dict = json.load(f)
