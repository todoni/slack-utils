import json
import os

import requests
from dotenv import load_dotenv

import scrum_bot
import slack_api

load_dotenv()

if __name__ == '__main__':
    scrum_file = open("scrum_payload.json")
    scrum_payload = scrum_file.read()
    token = os.environ.get('SLACK_BOT_USER_OAUTH_TOKEN')
    slack = slack_api.slack_api(token)
    parsed_data = json.loads(scrum_payload)
    blocks = parsed_data.get("blocks", [])

    slack.post_interactive_message(payload=blocks)
