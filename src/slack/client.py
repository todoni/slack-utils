class slack_client:
    def __init__(self, token):
        self.token = token

    def get_channel_id(self, channel_name, channel_types):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def get_member_name_by_id(self, member_id):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def get_channel_member_ids(self, channel_id):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def get_channel_member_names(self, member_ids):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def post_thread(self, channel_id, text):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def post_thread_interactive(self, channel_id, blocks):
        raise NotImplementedError(
            "This method should be implemented by subclasses")

    def open_modal(self, payload):
        raise NotImplementedError(
            "This method should be implemented by subclasses")
