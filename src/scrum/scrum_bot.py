import json
import os
import sys

import slack_api
from constants import (SCRUM_INITIATE_FILE_NAME, TEST_CHANNEL_NAME,
                       TYPE_PRIVATE_CHANNEL_ONLY)


class scrum_bot():
    def __init__(self, token):
        self.__initialize(token)

    def __initialize(self, token):
        # self.token = token
        scrum_initiate_message_file = open(
            SCRUM_INITIATE_FILE_NAME)
        self.__slack_client = slack_api.slack_api(token)
        self.channel_id = self.__slack_client.get_channel_id(
            TEST_CHANNEL_NAME, TYPE_PRIVATE_CHANNEL_ONLY)
        scrum_initiate_message_json = scrum_initiate_message_file.read()
        self.scrum_initiate_message_payload = json.loads(
            scrum_initiate_message_json).get("blocks", [])

    def initiate_scrum(self):
        member_ids = self.__slack_client.get_channel_member_ids(
            self.channel_id)
        for member_id in member_ids:
            result = self.__slack_client.post_interactive_message(
                channel=member_id, payload=self.scrum_initiate_message_payload)

    def post_scrum_to_channel(self, payload):
        payload['blocks'].pop()
        payload_without_button = jsonify(payload)
        self.slack.post_interactive_message(payload_without_button)
