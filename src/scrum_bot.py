import os

import slack_api


class scrum_bot:
    def __init__(self, token):
        self.token = token

    def run_scrum_bot():
        token = os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN")
        slack = slack_api.slack_api(token)
        channel_name = os.environ.get("SCRUM_CHANNEL_NAME")
        channel_id = slack.get_channel_id(channel_name, "private_channel")
        scrum_file = open("scrum.txt")
        scrum_body = scrum_file.read()
        scrum_head = "<!channel> Today's Scrum has arrived! :love_letter:\n\n" + scrum_body + "\n"
        members_display_name = slack.get_channel_members(channel_id)
        # slack.post_thread(channel_id, scrum_head)
        for name in members_display_name:
            text = ":sparkles: " + name
            # slack.post_thread(channel_id, text)
