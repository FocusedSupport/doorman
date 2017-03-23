import time
import json
import requests

from pydispatch import dispatcher

from ..dispatcher.signals import Signals


class SlackSender(object):

    # this one posts to #doormantest for now
    webhook_url = 'https://hooks.slack.com/services/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'

    def __init__(self):
        dispatcher.connect(self._handle_message, signal=Signals.SLACK_MESSAGE, sender=dispatcher.Any)
        self._run()

    def _handle_message(self, msg=None, img=None):
        formatted_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
        slack_data = {"username": "doorman", "text": ":door: [" + formatted_time + "]: " + msg}

        response = requests.post(
            self.webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            print("Error posting to slack")

        if img is not None:
            # upload/post?
            pass

    def _run(self):
        while True:
            time.sleep(10)
