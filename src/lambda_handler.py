import json
import logging
import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class lambda_handler:
    def __init__(self):
        pass

    def lambda_test(event, context):
        logger.info(json.dumps(event))
