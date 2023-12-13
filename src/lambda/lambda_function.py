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

        # Slack API endpoint and headers
        url = 'https://slack.com/api/chat.postMessage'
        headers = {
            'Authorization': f"Bearer {os.environ['SLACK_BOT_TOKEN']}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Slack message payload
        payload = {
            'channel': 'C04FL23CYNS',
            'text': 'Hello from AWS Lambda!',
        }
        payload_encoded = urllib.parse.urlencode(payload).encode('utf-8')
        # Create a request object
        req = urllib.request.Request(
            url, data=payload_encoded, headers=headers, method='POST')

        # Make the request to Slack API
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')

            # Check response from Slack
            if response.getcode() == 200:
                logger.info("Message sent to Slack successfully.")
                logger.info(response_body)
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
