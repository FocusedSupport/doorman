import time

from pydispatch import dispatcher

from ..dispatcher.signals import Signals


class MessageBuilder(object):

    def __init__(self):
        dispatcher.connect(self._handle_message, signal=Signals.PICTURE, sender=dispatcher.Any)
        self._run()

    def _handle_message(self, img=None):
        message = "Doorbell ring [main]"
        self._send_message(msg=message, img=img)

    def _send_message(self, msg=None, img=None):
        dispatcher.send(signal=Signals.SLACK_MESSAGE, sender=self, msg=msg, img=img)

    def _run(self):
        while True:
            time.sleep(10)