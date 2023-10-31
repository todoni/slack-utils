import os

import slack_api


def run_scrum_bot():
    token = os.environ.get("SLACK_BOT_USER_OAUTH_TOKEN")
    slack = slack_api.slack_api(token)
    channel_name = os.environ.get("SCRUM_CHANNEL_NAME")
    channel_id = slack.get_channel_id("daily-scrum", "private_channel")
    slack.post_thread(channel_id, "test")
