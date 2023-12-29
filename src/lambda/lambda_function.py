import base64
import json
import logging
import os
import urllib.parse
import urllib.request

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def post_response_message(blocks, channel):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': f"Bearer {os.environ['SLACK_BOT_TOKEN']}",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'channel': channel,
        'blocks': blocks,
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


def on_modal_submit(payload):
    logger.info(json.dumps(payload))
    callback_id = payload['view']['callback_id']
    if callback_id == "scrum-modal":
        answers = payload['view']['state']['values']
        logger.info(json.dumps(answers))
        answers = list(enumerate(answers.values()))
        # logger.info("***************index**************")
        # logger.info(indexes)
        logger.info("***************answers**************")
        logger.info(answers)
        first = "*1. How is your condition today?*\n" + \
            answers[0][1]['checkboxes-action']['selected_option']['text']['text'] + "\n\n"
        logger.info("first")
        second = "*2. What did you do since yesterday?*\n" + \
            answers[1][1]['plain_text_input-action']['value'] + "\n\n"
        third = "*3. What do you plan to do today?*\n" + \
            answers[2][1]['plain_text_input-action']['value'] + "\n\n"
        forth = "*4. Anything blocking your progress?*\n" + \
            answers[3][1]['plain_text_input-action']['value'] + "\n\n"

        message_blocks = [
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": first + second + third + forth
                }
            }
        ]

        message_block_as_string = json.dumps(message_blocks)
        logger.info(message_blocks)
        logger.info(message_block_as_string)
        url = 'https://slack.com/api/conversations.list'
        headers = {
            'Authorization': f"Bearer {os.environ['SLACK_BOT_TOKEN']}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        req = urllib.request.Request(
            url, headers=headers, method='GET')

        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')

        if response.getcode() == 200:
            logger.info("Listed channel successfully.")
            logger.info(response_body)
        else:
            logger.error(f"Error listing channels Slack: {response_body}")

        data = json.loads(response_body)
        channels = data['channels']
        channel = list(
            filter(lambda c: c["name"] == "random", channels))[0]
        channel_id = channel["id"]
        post_response_message(message_block_as_string, channel_id)


def lambda_handler(event, context):
    try:
        logger.info(json.dumps(event))
        body = base64.b64decode(event['body'])
        body_str = body.decode('utf-8').replace('+', ' ')
        decoded_body = urllib.parse.unquote(body_str)
        payload = json.loads(decoded_body.split('payload=', 1)[1])
        event_type = payload['type']

        if event_type == "block_actions":
            action_id = payload['actions'][0]['value']
            if action_id == "open_scrum_modal":
                trigger_id = payload['trigger_id']
                view_file = open("scrum_modal_payload.json")
                view_json = view_file.read()
                view_as_dict = json.loads(view_json)
                view_as_string = json.dumps(view_as_dict)
                open_modal(trigger_id, view_as_string)
        elif event_type == "view_submission":
            on_modal_submit(payload)

    except Exception as e:
        logger.error(f"Error: {str(e)}")

    return {
        'statusCode': 200
    }

# Additional functions or classes can be defined below
