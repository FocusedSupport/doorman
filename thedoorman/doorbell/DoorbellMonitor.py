import _thread
import time
import RPi.GPIO as GPIO

class DoorbellMonitor(object):

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
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        while True:
            input_state = GPIO.input(17)
            if input_state == False:
                print('Button Pressed')
                time.sleep(0.2)
