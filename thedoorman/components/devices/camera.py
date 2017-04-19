import time
from PIL import Image
from picamera import PiCamera
from io import BytesIO

from pydispatch import dispatcher
from ..dispatcher.signals import Signals


class Camera(object):

    IMG_FORMAT = 'png'

    def __init__(self):
        dispatcher.connect(self._handle_doorbell, signal=Signals.DOORBELL, sender=dispatcher.Any)
        dispatcher.connect(self._handle_request, signal=Signals.PICTURE_REQUEST, sender=dispatcher.Any)
        self._run()

    def _handle_doorbell(self):
        img = self._take_picture()
        self._send_message(img=img, source="doorbell")

    def _handle_request(self, username):
        img = self._take_picture()
        self._send_message(img=img, source="Picture request from " + username)

    def _run(self):
        while True:
            time.sleep(10)

    def _take_picture(self):
        with PiCamera() as camera:
            stream = BytesIO()
            #camera.start_preview()
            camera.capture(stream, format=Camera.IMG_FORMAT)
            # "Rewind" the stream to the beginning so we can read its content
            stream.seek(0)
            img = Image.open(stream)
            print("Took image at time %f" % time.time())
            return img

    def _send_message(self, img=None, source=None):
        dispatcher.send(signal=Signals.PICTURE, sender=self, img=img, source=source)
