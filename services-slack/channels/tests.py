import json

from django.test import TestCase
from django.urls import reverse


MEMBER_JOINED_CHANNEL_EVENT = {
    "token": "token",
    "team_id": "team_1234",
    "api_app_id": "api_app_1234",
    "event": {
        "type": "member_joined_channel",
        "user": "user_1234",
        "channel": "channel_1234",
        "channel_type": "C",
        "team": "team_1234",
        "event_ts": "1587671222.000700",
    },
    "type": "event_callback",
    "event_id": "event_1234",
    "event_time": 1587671222,
    "authed_users": ["user_1234"],
}


class MemberViewTests(TestCase):
    def test_post_event_returns_200(self):
        response = self.client.post(
            reverse("channels:member"),
            MEMBER_JOINED_CHANNEL_EVENT,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
