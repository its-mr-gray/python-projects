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

import utilities
from handlers import EVENT_HANDLERS
from variables import json_file, push_count, req

data = utilities.open_url(req)

# creates a file if it doesn't exist, does nothing if it does.
utilities.create_and_write_json(json_file, data)

for event in data:
    handlers = EVENT_HANDLERS.get(event["type"])
    if handlers:
        output_string = handlers(event)
        if event["type"] == "PushEvent":
            continue
        print(output_string)

if push_count:
    for repo, count in push_count.items():
        print(f"pushed {count} commits to {repo}\n")
"""
def interpret_output(data):
    push_count = {}
    # iterate over all the stuff from the data object
    for event in data:
        format_options = {}
        repo_name = event["repo"]["name"]
        count = event["payload"].get("size", 0)
        event_type = event["type"]
        # check if the event type exists in our template registry's keys
        if event_type == "PushEvent":
            if repo_name not in push_count:
                push_count[repo_name] = 0
            push_count[repo_name] += count

        elif event_type in event_template_registry.keys():
            # iterate over the required fields in our template registry
            for required_field in event_template_registry[event_type]["requires"]:
                required_value = get_nested(event["payload"], required_field)
                print(format_options)
            format_options["repo"] = repo_name

            if any(format_options.get(field) is None for field in required_field):
                format_options[required_field] = required_value
            print(
                event_template_registry[event_type]["template"].format(**format_options)
            )
        # activity_output = event_template_registry[event_type]["template"].format(
        #     **format_options
        # )

        #        print(format_options)

        # print(activity_output, output_string)


def count_of_push_events(data: dict, push_count: dict):
    for repo in push_count.keys():
        data = {"count": push_count[repo], "repo": repo}
        format_options = push_count['count']
        output_string = event_template_registry["PushEvent"]["template"].format(
            **format_options
        )


def get_nested(d, key, default=None):
    keys = key.split(".")
    for k in keys:
        if isinstance(d, dict):  # much better way of checking types
            d = d.get(k, default)
        else:
            return default
    return d
"""

if __name__ == "__main__":
    pass
