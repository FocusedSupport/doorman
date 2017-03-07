import _thread
import time
import RPi.GPIO as GPIO

class DoorbellMonitor(object):

    lastTime = 0
    ignoreTimeSeconds = 5.0
    BUTTON_CHANNEL = 17

    def __init__(self):
        print("I'm like a constructor!")
        self._count = 0

    def run(self):
        try:
            _thread.start_new_thread(self._monitor, tuple())
        except _thread.error:
            print("Error starting Doorbell Monitor thread")

    def _monitor(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        while True:
            channel = GPIO.wait_for_edge( self.BUTTON_CHANNEL, GPIO.RISING )
            currentTime = time.time()
            if currentTime - self.lastTime > self.ignoreTimeSeconds:
                print('Button Pressed callback')
                self.lastTime = currentTime

