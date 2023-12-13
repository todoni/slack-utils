import base64
import json
import logging
import os
import urllib.parse
import urllib.request

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def post_response_message(text, channel):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': f"Bearer {os.environ['SLACK_BOT_TOKEN']}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'channel': channel,
        'text': text,
    }
    payload_encoded = urllib.parse.urlencode(payload).encode('utf-8')

    req = urllib.request.Request(
        url, data=payload_encoded, headers=headers, method='POST')

    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode('utf-8')

        if response.getcode() == 200:
            logger.info("Message sent to Slack successfully.")
            logger.info(response_body)
        else:
            logger.error(f"Error sending message to Slack: {response_body}")


def open_modal(trigger_id):
    url = "https://slack.com/api/views.open"
    headers = {
        'Authorization': f"Bearer {os.environ['SLACK_BOT_TOKEN']}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        "trigger_id": trigger_id,
        "view": {
            "type": "modal",
            "callback_id": "modal-identifier",
            "title": {
                "type": "plain_text",
                "text": "Just a modal"
            },
            "blocks": [
                {
                    "type": "section",
                    "block_id": "section-identifier",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Welcome* to ~my~ Block Kit _modal_!"
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Just a button"
                        },
                        "action_id": "button-identifier"
                    }
                }
            ]
        }
    }

    payload_encoded = urllib.parse.urlencode(payload).encode('utf-8')

    req = urllib.request.Request(
        url, data=payload_encoded, headers=headers, method='POST')

    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode('utf-8')

        if response.getcode() == 200:
            logger.info(response_body)
        else:
            logger.error(f"Error sending message to Slack: {response_body}")


def lambda_handler(event, context):
    try:
        logger.info(json.dumps(event))
        body = base64.b64decode(event['body'])

        decoded_body = urllib.parse.unquote(body)

        payload = json.loads(decoded_body.split('payload=', 1)[1])
        trigger_id = payload['trigger_id']

        post_response_message('Hello from AWS Lambda!', 'C04FL23CYNS')
        open_modal(trigger_id)

    except Exception as e:
        logger.error(f"Error: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully!')
    }

# Additional functions or classes can be defined below
