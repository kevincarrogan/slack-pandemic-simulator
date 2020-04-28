from django.test import TestCase
from django.urls import reverse

from channels.models import Channel
from members.tests.factories import MemberFactory
from teams.models import Team

from .models import Message

TEAM_ID = "team_1234"
CHANNEL_ID = "channel_1234"
USER_ID = "user_1234"
BOT_USER_ID = "bot_1234"
MESSAGE_TIMESTAMP = "1588016001.000200"

MESSAGE_EVENT = {
    "token": "token",
    "team_id": TEAM_ID,
    "api_app_id": "api_app_1234",
    "event": {
        "client_msg_id": "9fd59457-1f74-4e43-9151-7c92d43ea7b3",
        "type": "message",
        "text": "hello",
        "user": USER_ID,
        "ts": MESSAGE_TIMESTAMP,
        "team": TEAM_ID,
        "channel": CHANNEL_ID,
        "event_ts": MESSAGE_TIMESTAMP,
        "channel_type": "channel",
    },
    "type": "event_callback",
    "event_id": "event_1234",
    "event_time": 1588016001,
    "authed_users": [USER_ID],
}


class MessageViewTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(bot_user_id=BOT_USER_ID, team_id=TEAM_ID)
        self.channel = Channel.objects.create(slack_id=CHANNEL_ID, team=self.team)
        self.member = MemberFactory.create(slack_id=USER_ID, team=self.team)

    def test_post_message_returns_200(self):
        self.assertEqual(Message.objects.count(), 0)

        response = self.client.post(
            reverse("messages:message"), MESSAGE_EVENT, content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

    def test_creates_message_object(self):
        self.assertEqual(Message.objects.count(), 0)

        response = self.client.post(
            reverse("messages:message"), MESSAGE_EVENT, content_type="application/json",
        )

        message = Message.objects.get()
        self.assertEqual(message.channel, self.channel)
        self.assertEqual(message.member, self.member)
        self.assertEqual(message.slack_timestamp, MESSAGE_TIMESTAMP)
