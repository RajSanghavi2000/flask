import requests
import json

__all__ = ['SlackWeb']


class SlackWeb:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.response = None

    def post_text(self, text):
        payload = {
            "text": text
        }
        response = self._request(payload)
        return response

    def post_attachments(self, text, attachments):
        payload = {
            "text": text,
            "attachments": attachments
        }
        response = self._request(payload)
        return response

    def block_post(self, blocks):
        response = self._request(blocks)
        return response

    def _request(self, payload):
        headers = {'content-type': 'application/json'}
        response = requests.post(
            self.webhook_url, data=json.dumps(payload), headers=headers)
        self.response = response
        return response
