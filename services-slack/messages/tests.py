import datetime

from unittest.mock import patch

from django.test import override_settings, TestCase
from django.urls import reverse

from channels.models import Channel
from members.tests.factories import MemberFactory
from teams.models import Team

from .models import Message

TEAM_ID = "team_1234"
CHANNEL_ID = "channel_0001"
USER_ID = "user_0001"
BOT_USER_ID = "bot_0001"
MESSAGE_TIMESTAMP = "1588016001.000200"
APP_ID = "api_app_0001"


def create_message_event(
    message_timestamp=MESSAGE_TIMESTAMP, user_id=USER_ID, additional_event_info=None
):
    event = {
        "client_msg_id": "9fd59457-1f74-4e43-9151-7c92d43ea7b3",
        "type": "message",
        "text": "hello",
        "user": user_id,
        "ts": message_timestamp,
        "team": TEAM_ID,
        "channel": CHANNEL_ID,
        "event_ts": message_timestamp,
        "channel_type": "channel",
    }

    if additional_event_info:
        event.update(additional_event_info)

    return {
        "token": "token",
        "team_id": TEAM_ID,
        "api_app_id": APP_ID,
        "event": event,
        "type": "event_callback",
        "event_id": "event_1234",
        "event_time": 1588016001,
        "authed_users": [user_id],
    }


MESSAGE_EVENT = create_message_event()

MESSAGE_SUB_TYPE_EVENT = create_message_event(
    additional_event_info={
        "subtype": "channel_join",
        "text": f"<@{USER_ID}> has joined the channel",
        "inviter": USER_ID,
    },
)


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

    def test_doesnt_create_message_for_sub_types(self):
        self.assertEqual(Message.objects.count(), 0)

        response = self.client.post(
            reverse("messages:message"),
            MESSAGE_SUB_TYPE_EVENT,
            content_type="application/json",
        )

        self.assertEqual(Message.objects.count(), 0)

    @override_settings(CONTACT_TIMEDELTA=datetime.timedelta(minutes=2))
    def test_post_to_contact_service_when_messages_overlap(self):
        message_time = datetime.datetime(2018, 9, 27)
        Message.objects.create(
            channel=self.channel,
            member=self.member,
            slack_timestamp=f"{int(message_time.timestamp())}.000200",
        )

        another_member = MemberFactory.create(slack_id="user_0002", team=self.team,)

        overlapping_message_time = message_time + datetime.timedelta(minutes=1)
        overlapping_message_event = create_message_event(
            message_timestamp=f"{int(overlapping_message_time.timestamp())}.000200",
            user_id=another_member.slack_id,
        )

        with patch("messages.views.service_request") as mock_service_request:
            self.client.post(
                reverse("messages:message"),
                overlapping_message_event,
                content_type="application/json",
            )
        mock_service_request.assert_called_once()
        service_name, end_point, payload = mock_service_request.call_args[0]
        self.assertEqual(
            service_name, "contact",
        )
        self.assertEqual(
            end_point, "/contact/",
        )
        members = [self.member, another_member]
        person_ids = [str(m.person_id) for m in members]
        self.assertEqual(
            set(payload["people_ids"]), set(person_ids),
        )

    @override_settings(CONTACT_TIMEDELTA=datetime.timedelta(minutes=2))
    def test_no_post_to_contact_service_when_messages_dont_overlap(self):
        message_time = datetime.datetime(2018, 9, 27)
        Message.objects.create(
            channel=self.channel,
            member=self.member,
            slack_timestamp=f"{int(message_time.timestamp())}.000200",
        )

        another_member = MemberFactory.create(slack_id="user_0002", team=self.team,)
        Message.objects.create(
            channel=self.channel,
            member=self.member,
            slack_timestamp=f"{int(message_time.timestamp())}.000400",
        )

        message_poster_member = MemberFactory.create(
            slack_id="user_0003", team=self.team,
        )
        overlapping_message_time = message_time + datetime.timedelta(minutes=3)
        overlapping_message_event = create_message_event(
            message_timestamp=f"{int(overlapping_message_time.timestamp())}.000200",
            user_id=message_poster_member.slack_id,
        )

        with patch("messages.views.service_request") as mock_service_request:
            self.client.post(
                reverse("messages:message"),
                overlapping_message_event,
                content_type="application/json",
            )
        mock_service_request.assert_not_called()

    @override_settings(CONTACT_TIMEDELTA=datetime.timedelta(minutes=2))
    def test_post_to_contact_service_when_multiple_messages_overlap(self):
        message_time = datetime.datetime(2018, 9, 27)
        Message.objects.create(
            channel=self.channel,
            member=self.member,
            slack_timestamp=f"{int(message_time.timestamp())}.000200",
        )

        another_member = MemberFactory.create(slack_id="user_0002", team=self.team,)
        Message.objects.create(
            channel=self.channel,
            member=another_member,
            slack_timestamp=f"{int(message_time.timestamp())}.000400",
        )

        message_poster_member = MemberFactory.create(
            slack_id="user_0003", team=self.team,
        )

        overlapping_message_time = message_time + datetime.timedelta(minutes=1)
        overlapping_message_event = create_message_event(
            message_timestamp=f"{int(overlapping_message_time.timestamp())}.000200",
            user_id=message_poster_member.slack_id,
        )

        with patch("messages.views.service_request") as mock_service_request:
            self.client.post(
                reverse("messages:message"),
                overlapping_message_event,
                content_type="application/json",
            )

        self.assertEqual(mock_service_request.call_count, 2)

        # We don't really care what order we make the calls in regards to the ids that are sent through so we can just check each one does exists and pop it off when we find it
        payloads = {
            frozenset([message_poster_member.person_id, self.member.person_id]),
            frozenset([message_poster_member.person_id, another_member.person_id]),
        }

        for call in mock_service_request.call_args_list:
            service_name, end_point, payload = call[0]
            self.assertEqual(service_name, "contact")
            self.assertEqual(end_point, "/contact/")
            people_ids = frozenset(payload["people_ids"])
            self.assertIn(people_ids, payloads)
            payloads.remove(people_ids)

        self.assertEqual(len(payloads), 0)
