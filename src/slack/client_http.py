import os
import urllib.parse
import urllib.request

from .client import slack_client


class client_http(slack_client):
    def __init__(self, token):
        super().__init__(token)
        self.base_url = "https://slack.com/api/"
        self.headers = {
            'Authorization': f"Bearer {os.environ['SLACK_BOT_TOKEN']}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def send_request(self, endpoint, payload=None, method='POST'):
        url = self.base_url + endpoint
        if payload:
            payload_encoded = urllib.parse.urlencode(payload).encode('utf-8')
        else:
            payload_encoded = None

        req = urllib.request.Request(
            url, data=payload_encoded, headers=self.headers, method=method)

        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')
            if response.getcode() == 200:
                logger.info("Request successful.")
                return json.loads(response_body)
            else:
                logger.error(f"Error in request: {response_body}")
                return None

    def get_channel_id(self, channel_name, channel_types):
        data = self.send_request('conversations.list', method='GET')
        channels = data['channels']
        channel = list(
            filter(lambda c: c["name"] == "random", channels))[0]
        channel_id = channel["id"]
        return channel_id

    def post_thread_interactive(self, channel_id, blocks):
        payload = {
            'channel': channel_id,
            'blocks': blocks
        }
        self.send_request("chat.postMessage", payload)

    def open_modal(self, trigger_id, view):
        payload = {
            'trigger_id': trigger_id,
            'view': view
        }
        self.send_request("views.open", payload)
