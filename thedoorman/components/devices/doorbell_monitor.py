import time

import RPi.GPIO as GPIO

from pydispatch import dispatcher
from ..dispatcher.signals import Signals, Senders
from .gpio import Pins


class DoorbellMonitor(object):

    def __init__(self):
        self.lastTime = 0
        self.ignoreTimeSeconds = 5.0
        dispatcher.connect(self._handle_lockevent, signal=Signals.UNLOCKED, sender=Senders.Any)
        dispatcher.connect(self._handle_lockevent, signal=Signals.LOCKED, sender=Senders.Any)
        self._run()

    def _handle_lockevent(self, door=None):
        print("received lock event, setting lastTime to now, to prevent doorbell")
        self.lastTime = time.time()

    def _run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Pins.BUTTON_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        while True:
            GPIO.wait_for_edge(Pins.BUTTON_CHANNEL, GPIO.RISING)
            currentTime = time.time()
            if currentTime - self.lastTime > self.ignoreTimeSeconds:
                self.lastTime = currentTime
                self._notify()

    def _notify(self):
        dispatcher.send(signal=Signals.DOORBELL, sender=self)