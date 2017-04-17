import time

from pydispatch import dispatcher

from ..dispatcher.signals import Signals
import RPi.GPIO as GPIO

class GPIOCleanup(object):

    def __init__(self):
        dispatcher.connect(self._exit, signal=Signals.EXIT, sender=dispatcher.Any)
        self._run()


    def _exit(self):
        print("Resetting RPi GPIO")
        GPIO.cleanup()

    def _run(self):
        while True:
            time.sleep(10)