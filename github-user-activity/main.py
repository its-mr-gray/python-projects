"""
In this project, you will build a simple command line interface (CLI) to fetch the recent activity of a GitHub user and display it in the terminal.
This project will help you practice your programming skills, including working with APIs, handling JSON data, and building a simple CLI application.


Requirements

The application should run from the command line, accept the GitHub username as an argument, fetch the user’s recent activity using the GitHub API,
and display it in the terminal. The user should be able to:

    Provide the GitHub username as an argument when running the CLI.

    github-activity <username>

    Fetch the recent activity of the specified GitHub user using the GitHub API. You can use the following endpoint to fetch the user’s activity:

    # https://api.github.com/users/<username>/events
    # Example: https://api.github.com/users/kamranahmedse/events

    Display the fetched activity in the terminal.

    Output:
    - Pushed 3 commits to kamranahmedse/developer-roadmap
    - Opened a new issue in kamranahmedse/developer-roadmap
    - Starred kamranahmedse/developer-roadmap
    - ...

    You can learn more about the GitHub API here.
    Handle errors gracefully, such as invalid usernames or API failures.
    Use a programming language of your choice to build this project.
    Do not use any external libraries or frameworks to fetch the GitHub activity.

If you are looking to build a more advanced version of this project, you can consider adding features like filtering the activity by event type,
displaying the activity in a more structured format, or caching the fetched data to improve performance. You can also explore other endpoints of the GitHub API to fetch
additional information about the user or their repositories.
"""

import argparse
import json
import os
from collections import defaultdict

import requests

parser = argparse.ArgumentParser()
parser.add_argument(
    "username", metavar="username", help="enter a username to see activity"
)
args = parser.parse_args()


username = args.username
json_file = "github-activity.json"

url = f"https://api.github.com/users/{username}/events"
r = requests.get(url)
data: list = json.loads(r.text)

if not os.path.exists(json_file):
    with open(json_file, "w") as f:
        json.dump(data, f, indent=2)

activity_dict: dict = defaultdict(lambda: defaultdict(int))

for event in data:
    repo_name: str = event["repo"]["name"]
    event_type: str = event["type"]
    activity_dict[repo_name][event_type] += 1


if __name__ == "__main__":
    for repo, events in activity_dict.items():
        print(repo, dict(events))
