import time
import json
import requests
import os

from pydispatch import dispatcher
from slackbot import settings
from ..dispatcher.signals import Signals


class SlackSender(object):

    webhook_url = settings.WEBHOOK_URL

    def __init__(self):
        dispatcher.connect(self._handle_message, signal=Signals.SLACK_MESSAGE, sender=dispatcher.Any)
        self._run()

    def _post_image_from_file(self, filename, token, channels, comment):
        f = {'file': (filename, open(filename, 'rb'), 'image/png', {'Expires': '0'})}
        response = requests.post(url='https://slack.com/api/files.upload', data=
        {'token': token, 'channels': channels, 'media': f, 'initial_comment': comment},
                                 headers={'Accept': 'application/json'}, files=f)
        return response.text

    def _post_image(self, img, msg):
        token = settings.API_TOKEN
        filename = "/tmp/DoorPicture-" + time.strftime("%Y%m%d-%H%M%S") + ".png"
        img.save(filename)
        self._post_image_from_file(filename=filename, token=token, channels=settings.IMG_CHANNEL, comment=msg)
        os.remove(filename)

    def _handle_message(self, msg=None, img=None):
        formatted_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
        formatted_msg = ":door: [" + formatted_time + "]: " + msg

        if img is not None:
            # upload/post?
            self._post_image(img=img, msg=formatted_msg )
        else:
            slack_data = {"username": "doorman", "text": formatted_msg}

            print("Posting slack message at %f" % time.time())
            response = requests.post(
                self.webhook_url, data=json.dumps(slack_data),
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code != 200:
                print("Error posting to slack")

    def _run(self):
        while True:
            time.sleep(10)
