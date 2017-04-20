import time

from pydispatch import dispatcher

from ..dispatcher.signals import Signals, Senders
from ..slack.user_manager import UserManager
import RPi.GPIO as GPIO
from .gpio import Pins

class Lock(object):

    def __init__(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Pins.MAIN_DOOR_RELAY_CHANNEL, GPIO.OUT)
        GPIO.setup(Pins.SIDE_DOOR_RELAY_CHANNEL, GPIO.OUT)

        self._lock(Pins.MAIN_DOOR_RELAY_CHANNEL)
        self._lock(Pins.SIDE_DOOR_RELAY_CHANNEL)

        dispatcher.connect(self._handle_message, signal=Signals.UNLOCK, sender=Senders.SLACKBOT)
        dispatcher.connect(self._cleanup, signal=Signals.CLEANUP, sender=dispatcher.Any)

        self._run()

    def _handle_message(self, door=None, duration=None, userid=None):
        username = UserManager().get_username(userid)

        if door.lower() == "main":
            button = Pins.MAIN_DOOR_RELAY_CHANNEL
        elif door.lower() == "side":
            button = Pins.SIDE_DOOR_RELAY_CHANNEL
        else:
            print("Unknown door " + door + ", not unlocking")
            return

        print("unlocking " + door + " for " + duration + " seconds, initiated by "+username)
        self._unlock(button)
        time.sleep(float(duration))
        self._lock(button)

    def _cleanup(self):
        print("locking up all doors in cleanup")
        self._lock(Pins.MAIN_DOOR_RELAY_CHANNEL)
        self._lock(Pins.SIDE_DOOR_RELAY_CHANNEL)

    def _lock(self, door):
        dispatcher.send(signal=Signals.LOCKED, sender=Senders.SLACKBOT, door=door)
        GPIO.output(door, GPIO.HIGH)

    def _unlock(self, door):
        dispatcher.send(signal=Signals.UNLOCKED, sender=Senders.SLACKBOT, door=door)
        GPIO.output(door, GPIO.LOW)

    def _run(self):
        while True:
            time.sleep(10)