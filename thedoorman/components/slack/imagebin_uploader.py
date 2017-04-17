import time
import os
import requests

from pydispatch import dispatcher

from ..dispatcher.signals import Signals


class ImagebinUploader(object):

    def __init__(self):
        dispatcher.connect(self._handle_message, signal=Signals.PICTURE, sender=dispatcher.Any)
        self._run()

    def _post_image_from_file(self, filename):
        files = {'file': (filename, open(filename, 'rb'), 'image/png')}
        response = requests.post(url='https://imagebin.ca/upload.php', files=files)
        url = self._getURL(response)
        if ( url == "" ):
            message = "unable to upload image!"
        else:
            message = url
        self._send_message(msg=message)

    def _getURL(self, response):
        lines=response.text.split("\n")
        for line in lines:
            if line.startswith( 'url:'):
                parts=line.split(":")
                return parts[1]
        return ""

    def _handle_message(self, img=None):
        if img == None:
            return
        filename = "/tmp/DoorPicture-" + time.strftime("%Y%m%d-%H%M%S") + ".png"
        img.save(filename)
        self._post_image_from_file(filename=filename)
        os.remove(filename)

    def _send_message(self, msg=None, img=None):
        dispatcher.send(signal=Signals.SLACK_MESSAGE, sender=self, msg=msg, img=img)

    def _run(self):
        while True:
            time.sleep(10)