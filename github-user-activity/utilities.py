def get_event(data, event_type):
    list_events = [
        data[i]["repo"]["name"]
        for i in range(len(data))
        if data[i]["type"] == event_type
    ]
    return list_events
