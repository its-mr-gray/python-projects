"""
variables.py

contains all applicable variables for CLI application
"""

from urllib.request import Request

from parsers import args

username: str = args.username
json_file = "github-activity.json"
headers = {"Accept": "application/vnd.github+json"}
url = f"https://api.github.com/users/{username}/events"
req = Request(url=url, headers=headers)

push_count = {}
