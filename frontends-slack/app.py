import logging

from slackeventsapi import SlackEventAdapter

from services import service_request
from settings import (
    DEBUG,
    SERVER_HOST,
    SERVER_PORT,
    SLACK_SIGNING_SECRET,
)

logger = logging.getLogger("events")
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, endpoint="/slack/events")


@slack_events_adapter.on("message")
def handle_message(event_data):
    logger.debug("handle_message %s", event_data)
    service_request("slack", "/message/", event_data)


@slack_events_adapter.on("member_joined_channel")
def handle_member_joined_channel(event_data):
    logger.debug("handle_member_joined_channel %s", event_data)
    service_request("slack", "/channel/member/", event_data)


slack_events_adapter.start(host=SERVER_HOST, port=SERVER_PORT, debug=DEBUG)
