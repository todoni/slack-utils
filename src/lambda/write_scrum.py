import base64
import json
import logging
import os
import urllib.parse
import urllib.request

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        # Log the received event
        logger.info(json.dumps(event))

        # body = base64.b64decode(event['body'])
        # body_str = body.decode('utf-8')

        # Parse the body to extract the payload
        # body_json = json.loads(body_str)
        # payload_data = body_json['payload']
        # logger.info(f"Extracted payload: {payload_data}")

        # Slack API endpoint and headers
        url = 'https://slack.com/api/chat.postMessage'
        headers = {
            'Authorization': f"Bearer {os.environ['SLACK_BOT_TOKEN']}",
            'Content-Type': 'application/json'
        }

        # Slack message payload
        payload = json.dumps({
            'channel': 'C04FL23CYNS',
            'text': 'Hello from AWS Lambda!',
            'response_type': 'in_channel'
        })

        # Create a request object
        req = urllib.request.Request(
            url, data=payload, headers=headers, method='POST')

        # Make the request to Slack API
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')

            # Check response from Slack
            if response.getcode() == 200:
                logger.info("Message sent to Slack successfully.")
                logger.info(response)
            else:
                logger.error(
                    f"Error sending message to Slack: {response_body}")

    except Exception as e:
        # Log any errors
        logger.error(f"Error: {str(e)}")

    # Return a response
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully!')
    }

# Additional functions or classes can be defined below
