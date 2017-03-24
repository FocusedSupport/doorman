import time

from pydispatch import dispatcher

from ..dispatcher.signals import Signals, Senders
from ..slack.user_manager import UserManager


class Lock(object):

    def __init__(self):
        dispatcher.connect(self._handle_message, signal=Signals.UNLOCK, sender=Senders.SLACKBOT)
        self._run()

    def _handle_message(self, door=None, duration=None, userid=None):
        username = UserManager().get_username(userid)
        print("unlock: " + door + " for " + duration + " seconds, initiated by "+username)

    def _run(self):
        while True:
            time.sleep(10)