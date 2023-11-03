import os

from slack_sdk import WebClient


class slack_api:
    def __init__(self, token):
        self.client = WebClient(token)

    def get_channel_id(self, channel_name, channel_types):
        result = self.client.conversations_list(
            types=channel_types)
        channels = result.data['channels']
        channel = list(
            filter(lambda c: c["name"] == channel_name, channels))[0]
        channel_id = channel["id"]
        return channel_id

    def get_channel_members(self, channel_id):
        result = self.client.conversations_members(channel=channel_id)
        members_id = result.data['members']
        scrum_bot_id = os.environ.get("SCRUM_BOT_ID")
        github_bot_id = os.environ.get("APP_GITHUB_BOT_ID")
        members_id.remove(scrum_bot_id)
        members_id.remove(github_bot_id)
        members_name = []
        for member_id in members_id:
            result = self.client.users_profile_get(user=member_id)
            profile = result.data['profile']
            print(member_id, profile)
            name = profile['display_name']
            if name == '':
                name = profile['real_name']
            members_name.append(name)
        return members_name

    def post_thread(self, channel_id, text):
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
        )
        return result
