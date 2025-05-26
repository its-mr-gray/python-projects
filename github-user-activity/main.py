"""
main.py

entry point for the github user activity CLI.
fetches and displays recent activity for a given github username

see README.md for more details
"""

import utilities
from handlers import EVENT_HANDLERS
from variables import json_file, push_count, req

data = utilities.open_url(req)
utilities.create_and_write_json(json_file, data)

if __name__ == "__main__":
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
