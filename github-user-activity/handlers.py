import utilities

EVENT_HANDLERS = {
    "PushEvent": utilities.get_push_events,
    "IssueCommentEvent": utilities.get_comment_events,
    "CommitCommentEvent": utilities.get_comment_events,
    "CreateEvent": utilities.get_create_events,
    "DeleteEvent": utilities.get_delete_events,
}
