import json
import os
import sys

import requests
from dotenv import load_dotenv
from scrum_bot import scrum_bot

import slack_api

load_dotenv()

if __name__ == '__main__':
    token = os.getenv("SLACK_BOT_USER_OAUTH_TOKEN")
    bot = scrum_bot(token=token)
    bot.initiate_scrum()
