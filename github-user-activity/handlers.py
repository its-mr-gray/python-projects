"""
handlers.py

uses current github API event types as dictionary keys and
matches them with corresponding function handlers as values
"""

import utilities

EVENT_HANDLERS = {
    "CommitCommentEvent": utilities.get_comment_events,
    "CreateEvent": utilities.get_create_events,
    "DeleteEvent": utilities.get_delete_events,
    "ForkEvent": utilities.get_fork_events,
    "GollumEvent": utilities.get_gollum_events,
    "IssuesEvent": utilities.get_issues_events,
    "IssueCommentEvent": utilities.get_comment_events,
    "MemberEvent": utilities.get_member_events,
    "PublicEvent": utilities.get_public_events,
    "PullRequestEvent": utilities.get_pull_request_events,
    "PullRequestReviewEvent": utilities.get_pull_request_review_events,
    "PullRequestReviewCommentEvent": utilities.get_pull_request_review_comment_events,
    "PullRequestReviewThreadEvent": utilities.get_pull_request_review_thread_events,
    "PushEvent": utilities.get_push_events,
    "ReleaseEvent": utilities.get_release_events,
    "SponsorshipEvent": utilities.get_sponsorship_events,
    "WatchEvent": utilities.get_watch_events,
}
