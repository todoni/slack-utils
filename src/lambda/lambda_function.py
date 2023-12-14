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


def open_modal(trigger_id, view):
    url = "https://slack.com/api/views.open"
    headers = {
        'Authorization': f"Bearer {os.environ['SLACK_BOT_TOKEN']}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        "trigger_id": trigger_id,
        "view": view
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
        view_file = open("scrum_modal_payload.json")
        view_json = view_file.read()
        view_as_string = json.loads(view_json)

        open_modal(trigger_id, view_as_string)

    except Exception as e:
        logger.error(f"Error: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully!')
    }

# Additional functions or classes can be defined below
