import json

from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from teams.models import Team

from .models import Channel

TEAM_ID = "team_1234"
CHANNEL_ID = "channel_1234"

MEMBER_JOINED_CHANNEL_EVENT = {
    "token": "token",
    "team_id": TEAM_ID,
    "api_app_id": "api_app_1234",
    "event": {
        "type": "member_joined_channel",
        "user": "user_1234",
        "channel": CHANNEL_ID,
        "channel_type": "C",
        "team": TEAM_ID,
        "event_ts": "1587671222.000700",
    },
    "type": "event_callback",
    "event_id": "event_1234",
    "event_time": 1587671222,
    "authed_users": ["user_1234"],
}

BOT_USER_ID = "bot_1234"

BOT_JOINED_CHANNEL_EVENT = {
    "token": "token",
    "team_id": TEAM_ID,
    "api_app_id": "api_app_1234",
    "event": {
        "type": "member_joined_channel",
        "user": BOT_USER_ID,
        "channel": CHANNEL_ID,
        "channel_type": "C",
        "team": TEAM_ID,
        "event_ts": "1587671222.000700",
    },
    "type": "event_callback",
    "event_id": "event_1234",
    "event_time": 1587671222,
    "authed_users": [BOT_USER_ID],
}


class MemberViewTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(bot_user_id=BOT_USER_ID, team_id=TEAM_ID)

    def test_post_event_returns_200(self):
        self.assertEqual(Channel.objects.count(), 0)

        response = self.client.post(
            reverse("channels:member"),
            MEMBER_JOINED_CHANNEL_EVENT,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Channel.objects.count(), 0)

    def test_bot_added_creates_channel_and_location(self):
        self.assertEqual(Channel.objects.count(), 0)

        response = self.client.post(
            reverse("channels:member"),
            BOT_JOINED_CHANNEL_EVENT,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)

        channel = Channel.objects.get()
        self.assertEqual(channel.team, self.team)
        self.assertEqual(channel.slack_id, CHANNEL_ID)
