import os

from flask import Blueprint, Flask, jsonify, request

import slack_api


class scrum_bot():
    def __init__(self, *args, **kwargs):
        super(scrum_bot, self).__init__(*args, **kwargs)
        self.initialize()

    def initialize(self):
        self.initialize_member_variables()
        self.initialize_route()
        self.initialize_interactive_handlers()

    def initialize_member_variables(self):
        token = os.environ.get('SLACK_BOT_USER_OAUTH_TOKEN')
        # channel_name = os.environ.get("SCRUM_CHANNEL_NAME")
        channel_name = "test-bot"
        scrum_file = open("scrum_payload.json")
        self.slack = slack_api.slack_api(token)
        self.channel_id = self.slack.get_channel_id(
            channel_name, "public_channel, private_channel")
        self.scrum_payload_init = scrum_file.read()

    def initialize_interactive_handlers(self):
        self.interactive_handlers = {
            'send-scrum-to-members': self.send_scrum_to_members,
            'post-scrum-to-channel': self.post_scrum_to_channel,
        }

    def initialize_route(self):
        self.interactive_bp = Blueprint(
            'interactive', __name__, url_prefix='/interactive')

        self.interactive_bp.route('/', methods=['POST'])(self.interactive)

        self.register_blueprint(self.interactive_bp)

    def interactive(self):
        post_data = request.form
        interactive_type = post_data.get('type')

        handler = self.interaction_handlers.get(interactive_type)
        if handler:
            response = handler(post_data)
            return jsonify(response)
        else:
            print("*************************************\n", response)
            return jsonify({"error": "Unknown interactive type"})

    def send_scrum_to_members(self):
        pass

    def post_scrum_to_channel(self):
        pass

    def run_scrum_bot(self):
        body = {
            "type": "send_scrum_to_members",
            "payload": self.scrum_payload_init
        }
        response = requests.post(
            "https://onedegreelabs.slack.com/interactive", data=body)
        if response.status_code == 200:
            return {"response": "Successfully sent scrum to members"}
        else:
            return {"error": "Failed to send scrum to members"}
