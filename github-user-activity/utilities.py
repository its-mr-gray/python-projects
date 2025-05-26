import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

from variables import push_count


def create_and_write_json(file, data):
    Path(file).touch()

    with open(file, "w") as f:
        json.dump(data, f, indent=2)


def open_url(request):
    try:
        with urlopen(request) as response:
            data = json.loads(response.read().decode())
    except HTTPError as e:
        print(f"error: {e.code} - {e.reason}")

    return data


def get_comment_events(event):
    user, repo_name = common_retrievals(event)
    comment = event["payload"].get("comment")
    comment_url = comment["html_url"]

    return f"{user} left a comment regarding {repo_name}.\ncomment url: {comment_url}\n"


def get_create_events(event):
    user, repo_name = common_retrievals(event)
    branch_or_tag = event["payload"].get("ref_type")
    name = event["payload"].get("ref")

    return f"{user} created a new {branch_or_tag} called {name} in {repo_name}"


def get_fork_events(event):
    fork = event["payload"].get("forkee")
    forked_name = fork["name"]
    original_repo = event["payload"].get("repository")
    original_name = original_repo["name"]
    fork_initiator = event["payload"].get("sender")
    user = fork_initiator["login"]

    return f"{user} forked repo {forked_name} from {original_name}"


def get_delete_events(event):
    user, repo_name = common_retrievals(event)
    branch_or_tag = event["payload"].get("ref_type")
    name = event["payload"].get("ref")

    return f"{user} deleted a {branch_or_tag} called {name} in {repo_name}"


def get_push_events(event):
    repo_name = event["repo"].get("name", "")
    count = event["payload"].get("size", 0)

    if repo_name not in push_count:
        push_count[repo_name] = 0
    push_count[repo_name] += count

    return push_count


def common_retrievals(event):
    user = event["actor"].get("display_login")
    repo_name = event["repo"].get("name")

    return user, repo_name
