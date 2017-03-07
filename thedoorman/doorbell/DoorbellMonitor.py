import _thread
import time


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
        while True:
            self._count += 1
            print(self._count)
            time.sleep(3)