import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import slack_api

def run_notification_bot():
    token = os.environ.get("SLACK_APP_MEETING_NOTIFICATION_TOKEN")
    slack = slack_api.slack_api(token)
    channel_name = os.environ.get("MEETING_NOFITICATION_CHANNEL_NAME")
    channel_id = slack.get_channel_id(channel_name, "private_channel")
    slack.post_thread(channel_id, "주간 스프린트 정기 회의가 2시간 후인 오후 7시에 시작됩니다! 🚀")