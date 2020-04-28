import itertools
import json

from slack import WebClient

from django.http import HttpResponse
from django.views import View

from members.models import Member
from services_slack.services import service_request
from teams.models import Team

from .models import Channel


class MemberView(View):
    def get_members_of_channel(self, channel):
        team = channel.team
        client = WebClient(token=team.bot_access_token)

        members_responses = (
            response["members"]
            for response in client.conversations_members(channel=channel.slack_id)
        )
        members = itertools.chain(*members_responses)
        members = (member for member in members if member != team.bot_user_id)

        return members

    def post(self, request):
        event = json.loads(request.body)
        event_data = event["event"]

        team = Team.objects.get(team_id=event["team_id"])

        if team.bot_user_id == event_data["user"]:
            channel, _ = Channel.objects.get_or_create(
                slack_id=event_data["channel"], team=team,
            )

            members = self.get_members_of_channel(channel)
            for member in members:
                try:
                    member = Member.objects.get(slack_id=member, team=team)
                except Member.DoesNotExist:
                    person_response = service_request("people", "/person/", {})
                    person_id = person_response["id"]
                    Member.objects.create(
                        person_id=person_id, slack_id=member, team=team,
                    )

        return HttpResponse("OK")
