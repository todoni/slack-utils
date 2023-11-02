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
        members_display_name = []
        for member_id in members_id:
            print("??????????", member_id)
            result = self.client.users_profile_get(id=member_id)
            members_display_name.append(result)
        print("*********")
        for name in members_display_name:
            print(name)
        # print(result)

        return result

    def post_thread(self, channel_id, text):
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
        )
        return result
