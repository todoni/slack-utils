import os

import slack_api


def run_scrum_bot():
    token = os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN")
    slack = slack_api.slack_api(token)
    channel_name = os.environ.get("SCRUM_CHANNEL_NAME")
    channel_id = slack.get_channel_id("test-bot", "private_channel")
    scrum_file = open("scrum.txt")
    scrum_text = scrum_file.read()
    slack.post_thread(channel_id, scrum_text)
    print("asdfasdfsa", channel_id, type(channel_id))
    result = slack.get_channel_members(channel_id)
