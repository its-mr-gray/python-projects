"""
The application should run from the command line, accept user actions and inputs as arguments, and store the tasks in a JSON file. The user should be able to:

    Add, Update, and Delete tasks
    Mark a task as in progress or done
    List all tasks
    List all tasks that are done
    List all tasks that are not done
    List all tasks that are in progress

Here are some constraints to guide the implementation:

    Use positional arguments in command line to accept user inputs.
    Use a JSON file to store the tasks in the current directory. <- DONE
    The JSON file should be created if it does not exist. <- DONE
    Use the native file system module of your programming language to interact with the JSON file.
    Do not use any external libraries or frameworks to build this project.
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

parser.add_argument("list", help="lists all tasks in your task tracker (:")

args = parser.parse_args()

with open(json_file, "r") as f:
    data = json.load(f)

if args.list:
    print(json.dumps(data, indent=2))
