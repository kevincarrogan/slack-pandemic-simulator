from slackeventsapi import SlackEventAdapter

from settings import (
    DEBUG,
    SERVER_HOST,
    SERVER_PORT,
    SLACK_SIGNING_SECRET,
)

slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, endpoint="/slack/events")


@slack_events_adapter.on("message")
def handle_message(event_data):
    print(event_data)
    message = event_data["event"]
    print(message)


@slack_events_adapter.on("member_joined_channel")
def handle_member_joined_channel(event_data):
    print(event_data)
    member_joined = event_data["event"]
    print(member_joined)


slack_events_adapter.start(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG)
