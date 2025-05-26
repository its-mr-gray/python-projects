"""
utilities.py

contains all functions used in CLI logic
"""

import json
from pathlib import Path
from typing import TextIO
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from variables import push_count


def create_and_write_json(file: TextIO, data: list[dict]) -> None:
    """
    creates a .json file if it doesn't exist and writes to it.

    args:
        file (TextIO): a .json file
        data (list[dict]): a list of github API events

    returns:
        None
    """
    Path(file).touch()

    with open(file, "w") as f:
        json.dump(data, f, indent=2)


def open_url(request: Request) -> list[dict]:
    """
    creates a json object from an HTTP request

    args:
        request (Request): a Request object from urllib requesting data from a given url

    returs:
        data (list): a list containing the result of the HTTP request
    """
    try:
        with urlopen(request) as response:
            data = json.loads(response.read().decode())
    except HTTPError as e:
        print(f"error: {e.code} - {e.reason}")

    return data


def get_comment_events(event: dict) -> str:
    """
    prints to the terminal github event comment information

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    user, repo_name = common_retrievals(event)
    comment = event["payload"].get("comment")
    comment_url = comment["html_url"]

    return f"{user} left a comment regarding {repo_name}.\ncomment url: {comment_url}\n"


def get_create_events(event: dict) -> str:
    """
    prints to the terminal github creation event information for github events

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event

    """
    user, repo_name = common_retrievals(event)
    branch_or_tag = event["payload"].get("ref_type")

    return f"{user} created a new {branch_or_tag} in {repo_name}\n"


def get_delete_events(event: dict) -> str:
    """
    prints to the terminal github deletion information for branches/tags

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    user, repo_name = common_retrievals(event)
    branch_or_tag = event["payload"].get("ref_type")
    name = event["payload"].get("ref")

    return f"{user} deleted a {branch_or_tag} called {name} in {repo_name}\n"


def get_fork_events(event: dict) -> str:
    """
    prints to the terminal information about forked repositories

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    fork = event["payload"].get("forkee")
    forked_name = fork["name"]
    original_repo = event["payload"].get("repository")
    original_name = original_repo["name"]
    fork_initiator = event["payload"].get("sender")
    user = fork_initiator["login"]

    return f"{user} forked repo {forked_name} from {original_name}\n"


def get_gollum_events(event: dict) -> str:
    """
    prints to the terminal information about updated wiki pages within a repository.

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    user, repo_name = common_retrievals(event)

    return f"{user} updated wiki pages in {repo_name}"


def get_issues_events(event: dict) -> str:
    """
    prints to the terminal information pertaining to github issues in a given repository

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    user, repo_name = common_retrievals(event)
    issue_action = event["payload"].get("action")
    issue = event["payload"].get("issue")
    issue_url = issue["html_url"]

    return f"{user} {issue_action} an issue in {repo_name}.\n issue url: {issue_url}\n"


def get_member_events(event: dict) -> str:
    """
    prints to the terminal information regarding repository collaborators.

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    repo_name = event["repo"].get("name")
    action = event["payload"].get("action")
    member = event["payload"].get("member")
    new_member_username = member["login"]
    granting_user = event["payload"].get("sender")
    granting_user_name = granting_user["login"]

    return f"{new_member_username} {action} to {repo_name} by {granting_user_name}\n"


def get_public_events(event: dict) -> str:
    """
    prints to the terminal repository privacy changes

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    user, repo_name = common_retrievals(event)

    return f"{user} changed {repo_name} from private to public."


def get_pull_request_events(event: dict) -> str:
    """
    prints to the terminal a user's pull request activity

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    user, repo_name = common_retrievals(event)
    action = event["payload"].get("action")
    pull_request_info = event["payload"].get("pull_request")
    pull_request_url = pull_request_info["html_url"]

    return f"{user} {action} pull request.\npull request url: {pull_request_url}\n"


def get_pull_request_review_events(event: dict) -> str:
    """
    prints to the terminal a user's interaction with pull request reviews

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    user, repo_name = common_retrievals(event)
    action = event["payload"].get("action")
    pull_request_info = event["payload"].get("pull_request")
    pull_request_url = pull_request_info["html_url"]

    return f"{user} {action} a review on a pull request in {repo_name}.\npull request url: {pull_request_url}\n"


def get_pull_request_review_comment_events(event: dict) -> str:
    """
    prints to the terminal a user's pull request comments

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    user, repo_name = common_retrievals(event)
    action = event["payload"].get("action")
    pull_request_info = event["payload"].get("pull_request")
    pull_request_url = pull_request_info["html_url"]

    return f"{user} {action} a comment on a pull request review.\npull request url: {pull_request_url}\n"


def get_pull_request_review_thread_events(event: dict) -> str:
    """
    prints to the terminal action taken on comment threads in a pull request

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    user, repo_name = common_retrievals(event)
    action = event["payload"].get("action")

    return f"{user} marked pull request comment thread as {action} in {repo_name}\n"


def get_push_events(event: dict) -> dict:
    """
    aggregates push event commits to a given repository

    args:
        event (dict): a single github event object

    returns:
        dict: an updated push_count dictionary containing push event aggregation
    """
    repo_name = event["repo"].get("name", "")
    count = event["payload"].get("size", 0)

    if repo_name not in push_count:
        push_count[repo_name] = 0
    push_count[repo_name] += count

    return push_count


def get_release_events(event: dict) -> str:
    """
    prints to the terminal release information for a given repository

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    user, repo_name = common_retrievals(event)
    action = event["payload"].get("action")
    release_info = event["payload"].get("release")
    release_url = release_info["html_url"]

    return f"{user} {action} a release in {repo_name}.\nrelease url: {release_url}\n"


def get_sponsorship_events(event: dict) -> str:
    """
    prints to the terminal user sponsorship information

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    action = event["payload"].get("action")
    sponsorship_info = event["payload"].get("sponsorship")
    sponsor_info = sponsorship_info["sponsor"].get("login")
    sponsored_info = sponsorship_info["sponsorable"].get("login")

    return f"{sponsor_info} {action} a sponsorship for {sponsored_info}\n"


def get_watch_events(event: dict) -> str:
    """
    prints to the terminal a user's starred repositories

    args:
        event (dict): a single github event object

    returns:
        str: a formatted, user-friendly string of information pertaining to the given event
    """
    user, repo_name = common_retrievals(event)

    return f"{user} starred {repo_name}\n"


def common_retrievals(event: dict) -> tuple[str, str]:
    """
    returns string values of commonly utilized github event items

    args:
        event (dict): a single github event object

    returns:
        tuple[str,str]: a tuple containg the string values of the commonly utilized items
    """
    user = event["actor"].get("display_login")
    repo_name = event["repo"].get("name")

    return user, repo_name
