import _thread
import time
import RPi.GPIO as GPIO
import json
import requests


class DoorbellMonitor(object):

    lastTime = 0
    ignoreTimeSeconds = 5.0
    BUTTON_CHANNEL = 17

    # this one posts to #doormantest for now
    webhook_url = 'https://hooks.slack.com/services/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'

    def __init__(self):
        print("I'm like a constructor!")
        self._count = 0

    def run(self):
        try:
            _thread.start_new_thread(self._monitor, tuple())
        except _thread.error:
            print("Error starting Doorbell Monitor thread")

    def temporaryNotify(self):
        formattedTime = time.strftime('%l:%M%p %Z on %b %d, %Y')
        slack_data = {"username": "doorman", "text": ":door: Someone is ringing the doorbell at " + formattedTime}

        response = requests.post(
            self.webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code != 200:
            print("Error posting to slack")

    def _monitor(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        while True:
            channel = GPIO.wait_for_edge( self.BUTTON_CHANNEL, GPIO.RISING )
            currentTime = time.time()
            if currentTime - self.lastTime > self.ignoreTimeSeconds:
                print('Button Pressed callback')
                self.temporaryNotify()
                self.lastTime = currentTime

