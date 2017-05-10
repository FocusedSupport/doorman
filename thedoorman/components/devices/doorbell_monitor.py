import time

import RPi.GPIO as GPIO

from time import sleep
from pydispatch import dispatcher
from ..dispatcher.signals import Signals, Senders
from .gpio import Pins


class DoorbellMonitor(object):

    def __init__(self):
        self.lastTime = 0
        self.ignoreTimeSeconds = 5.0
        self.bounce = 0.050   # in seconds
        dispatcher.connect(self._handle_unlockevent, signal=Signals.UNLOCKED, sender=dispatcher.Any)
        dispatcher.connect(self._handle_lockevent, signal=Signals.LOCKED, sender=dispatcher.Any)
        self._run()

    def _handle_lockevent(self, door=None):
        print("received lock event, setting lastTime to now, to prevent doorbell")
        self.lastTime = time.time()

    def _handle_unlockevent(self, door=None):
        print("received unlock event, setting lastTime to now, to prevent doorbell")
        self.lastTime = time.time()

    def _run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Pins.BUTTON_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        while True:
            GPIO.wait_for_edge(Pins.BUTTON_CHANNEL, GPIO.RISING)
            pinValue = GPIO.input(Pins.BUTTON_CHANNEL)

            print("input after rising edge at " + str(time.time()))
            sleep(self.bounce)
            pinValue = GPIO.input(Pins.BUTTON_CHANNEL)
            if pinValue == 0:
                print("skipping bouncing ring")
            else:
                currentTime = time.time()
                if currentTime - self.lastTime > self.ignoreTimeSeconds:
                    self.lastTime = currentTime
                    self._notify()

    def _notify(self):
        dispatcher.send(signal=Signals.DOORBELL, sender=self)