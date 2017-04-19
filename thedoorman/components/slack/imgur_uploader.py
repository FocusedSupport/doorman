import time
import os
from imgurpython import ImgurClient

from pydispatch import dispatcher

from ..dispatcher.signals import Signals



#image='DoorPicture-20170417-090258.png'

#client = ImgurClient(client_id, client_secret)

#client.upload_from_path(image)


class ImgurUploader(object):

    def __init__(self):
        self.client_id = '44c6da535071382'
        self.client_secret = 'eb1efc9b5f904ecc64ee8675a92e922777a86470'
        self.client = ImgurClient(self.client_id, self.client_secret)

        dispatcher.connect(self._handle_message, signal=Signals.PICTURE, sender=dispatcher.Any)
        self._run()

    def _post_image_from_file(self, filename, message):
        result = self.client.upload_from_path(filename)
        if 'link' in result:
            message += ": " + result['link']
            print("Uploaded image to URL " + result['link'] + " at time  %f" % time.time())
        else:
            message += ": unable to upload image!"

        self._send_message(msg=message)

    def _handle_message(self, img=None, source=None):
        if img == None:
            return
        if source == "doorbell":
            message = "Doorbell ring [main]"
        else:
            message = source
        print("Got image from " + source + " at time  %f" % time.time())
        filename = "/tmp/DoorPicture-" + time.strftime("%Y%m%d-%H%M%S") + ".png"
        img.save(filename)
        print("Saved image to file " + filename +" at time  %f" % time.time())

        self._post_image_from_file(filename=filename, message=message)
        os.remove(filename)

    def _send_message(self, msg=None, img=None):
        dispatcher.send(signal=Signals.SLACK_MESSAGE, sender=self, msg=msg, img=img)

    def _run(self):
        while True:
            time.sleep(10)