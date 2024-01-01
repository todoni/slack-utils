import json
import os
import sys

import requests
from dotenv import load_dotenv

from ..constants.scrum import (SCRUM_INITIATE_FILE_NAME, TEST_CHANNEL_NAME,
                               TYPE_PUBLIC_CHANNEL_ONLY)
from ..slack.client_sdk import client_sdk

load_dotenv()


class scrum_bot:
    def __init__(self, token):
        self.__initialize(token)

    def __initialize(self, token):
        # self.token = token
        scrum_initiate_message_file = open(
            SCRUM_INITIATE_FILE_NAME)
        self.__slack_client = client_sdk(token)
        self.channel_id = self.__slack_client.get_channel_id(
            TEST_CHANNEL_NAME, TYPE_PUBLIC_CHANNEL_ONLY)
        scrum_initiate_message_json = scrum_initiate_message_file.read()
        self.scrum_initiate_message_payload = json.loads(
            scrum_initiate_message_json).get("blocks", [])

    def initiate_scrum(self):
        member_ids = self.__slack_client.get_channel_member_ids(
            self.channel_id)
        for member_id in member_ids:
            result = self.__slack_client.post_thread_interactive(
                channel=member_id, payload=self.scrum_initiate_message_payload)

    # def post_scrum_to_channel(self, payload):
    #    payload['blocks'].pop()
    #    payload_without_button = jsonify(payload)
    #    self.slack.post_interactive_message(payload_without_button)


if __name__ == '__main__':
    token = os.getenv("SLACK_BOT_USER_OAUTH_TOKEN")
    print("****************************", token)
    print(os.environ)
    bot = scrum_bot(token=token)
    bot.initiate_scrum()
