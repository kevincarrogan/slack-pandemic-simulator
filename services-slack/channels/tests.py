import json
import uuid

from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from members.models import Member
from teams.models import Team

from .models import Channel

TEAM_ID = "team_1234"
CHANNEL_ID = "channel_1234"


def create_event(user_id, channel_id=CHANNEL_ID, team_id=TEAM_ID):
    return {
        "token": "token",
        "team_id": team_id,
        "api_app_id": "api_app_1234",
        "event": {
            "type": "member_joined_channel",
            "user": user_id,
            "channel": channel_id,
            "channel_type": "C",
            "team": team_id,
            "event_ts": "1587671222.000700",
        },
        "type": "event_callback",
        "event_id": "event_1234",
        "event_time": 1587671222,
        "authed_users": [user_id],
    }


MEMBER_JOINED_CHANNEL_EVENT = create_event("user_1234")

BOT_USER_ID = "bot_1234"

BOT_JOINED_CHANNEL_EVENT = create_event(BOT_USER_ID)


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

        with patch(
            "channels.views.WebClient.conversations_members"
        ) as mock_conversations_members:
            mock_conversations_members.return_value = []
            response = self.client.post(
                reverse("channels:member"),
                BOT_JOINED_CHANNEL_EVENT,
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 200)

        channel = Channel.objects.get()
        self.assertEqual(channel.team, self.team)
        self.assertEqual(channel.slack_id, CHANNEL_ID)

    def test_bot_added_creates_members_in_channel(self):
        self.assertEqual(Member.objects.count(), 0)

        member_0001_slack_id = "member_0001"
        member_0002_slack_id = "member_0002"

        with patch(
            "channels.views.WebClient.conversations_members"
        ) as mock_conversations_members, patch(
            "channels.views.service_request"
        ) as mock_service_request:
            mock_conversations_members.return_value = [
                {"members": [member_0001_slack_id]},
                {"members": [member_0002_slack_id]},
            ]

            person_0001_uuid = uuid.uuid4()
            person_0002_uuid = uuid.uuid4()
            people_ids = [person_0002_uuid, person_0001_uuid]

            def person_id(*args):
                return {"id": people_ids.pop()}

            mock_service_request.side_effect = person_id

            response = self.client.post(
                reverse("channels:member"),
                BOT_JOINED_CHANNEL_EVENT,
                content_type="application/json",
            )

        mock_conversations_members.assert_called_with(channel=CHANNEL_ID)
        mock_service_request.assert_called_with("people", "/person/", {})

        self.assertEqual(Member.objects.count(), 2)

        member_0001 = Member.objects.get(slack_id=member_0001_slack_id)
        self.assertEqual(member_0001.team, self.team)
        self.assertEqual(member_0001.person_id, person_0001_uuid)

        member_0002 = Member.objects.get(slack_id=member_0002_slack_id)
        self.assertEqual(member_0002.team, self.team)
        self.assertEqual(member_0002.person_id, person_0002_uuid)

    def test_bot_added_doesnt_create_member_for_bot_user(self):
        self.assertEqual(Member.objects.count(), 0)

        with patch(
            "channels.views.WebClient.conversations_members"
        ) as mock_conversations_members, patch(
            "channels.views.service_request"
        ) as mock_service_request:
            mock_conversations_members.return_value = [
                {"members": [BOT_USER_ID]},
            ]

            response = self.client.post(
                reverse("channels:member"),
                BOT_JOINED_CHANNEL_EVENT,
                content_type="application/json",
            )

        mock_conversations_members.assert_called_with(channel=CHANNEL_ID)

        self.assertEqual(Member.objects.count(), 0)

    def test_bot_added_doesnt_duplicate_members(self):
        person_0001_uuid = uuid.uuid4()
        member_0001_slack_id = "member_0001"
        member_0001 = Member.objects.create(
            slack_id=member_0001_slack_id, person_id=person_0001_uuid, team=self.team
        )
        self.assertEqual(Member.objects.count(), 1)

        with patch(
            "channels.views.WebClient.conversations_members"
        ) as mock_conversations_members, patch(
            "channels.views.service_request"
        ) as mock_service_request:
            mock_conversations_members.return_value = [
                {"members": [member_0001_slack_id]},
            ]

            def person_id(*args):
                people_ids = [person_0001_uuid]
                return {"id": people_ids.pop()}

            mock_service_request.side_effect = person_id

            response = self.client.post(
                reverse("channels:member"),
                BOT_JOINED_CHANNEL_EVENT,
                content_type="application/json",
            )

        mock_service_request.assert_not_called()

        self.assertEqual(Member.objects.count(), 1)

    def test_bot_added_duplicates_members_across_teams(self):
        person_0001_uuid = uuid.uuid4()
        member_0001_slack_id = "member_0001"
        member_0001 = Member.objects.create(
            slack_id=member_0001_slack_id, person_id=person_0001_uuid, team=self.team
        )
        self.assertEqual(Member.objects.count(), 1)

        other_team_id = "other_team_id_1234"
        team = Team.objects.create(bot_user_id=BOT_USER_ID, team_id=other_team_id)

        with patch(
            "channels.views.WebClient.conversations_members"
        ) as mock_conversations_members, patch(
            "channels.views.service_request"
        ) as mock_service_request:
            mock_conversations_members.return_value = [
                {"members": [member_0001_slack_id]},
            ]

            def person_id(*args):
                people_ids = [person_0001_uuid]
                return {"id": people_ids.pop()}

            mock_service_request.side_effect = person_id

            event = create_event(BOT_USER_ID, team_id=other_team_id)

            response = self.client.post(
                reverse("channels:member"), event, content_type="application/json"
            )

        self.assertEqual(Member.objects.count(), 2)
