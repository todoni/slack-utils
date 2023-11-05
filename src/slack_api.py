import json
import logging
import os

from slack_sdk import WebClient


class slack_api:
    def __init__(self, token):
        self.client = WebClient(token)

    def get_channel_id(self, channel_name, channel_types):
        result = self.client.conversations_list(
            types=channel_types)
        print("*********************************\n", result)
        channels = result.data['channels']
        channel = list(
            filter(lambda c: c["name"] == channel_name, channels))[0]
        channel_id = channel["id"]
        return channel_id

    def get_member_name_by_id(self, member_id):
        result = self.client.users_profile_get(user=member_id)
        profile = result.data['profile']
        print(member_id, profile)
        name = profile['display_name']
        if name == '':
            name = profile['real_name']
        return name

    def get_channel_member_ids(self, channel_id):
        result = self.client.conversations_members(channel=channel_id)
        member_ids = result.data['members']
        print("memberids", member_ids)
        scrum_bot_id = os.environ.get("SCRUM_BOT_ID")
        github_bot_id = os.environ.get("APP_GITHUB_BOT_ID")
        if scrum_bot_id in member_ids:
            member_ids.remove(scrum_bot_id)
        if github_bot_id in member_ids:
            member_ids.remove(github_bot_id)
        return member_ids

    def get_channel_member_names(self, member_ids):
        member_names = []
        for member_id in member_ids:
            result = self.client.users_profile_get(user=member_id)
            profile = result.data['profile']
            print(member_id, profile)
            name = profile['display_name']
            if name == '':
                name = profile['real_name']
            member_names.append(name)
        return member_names

    def post_thread(self, channel_id, text):
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
        )
        return result

    def post_interactive_message(self, channel, payload):
        result = self.client.chat_postMessage(
            as_user=True, channel=channel, blocks=payload)
        return result

    def send_DM(self, member_id, text):
        result = self.client.chat_postMessage(
            channel=member_id,
            text=text
        )
        return result

    def open_modal(self, payload):
        result = self.client.views_open(view=payload, trigger_id="test")
        return result
