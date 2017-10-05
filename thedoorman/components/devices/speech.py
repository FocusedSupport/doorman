import os
import time
import subprocess

from pydispatch import dispatcher
from ..dispatcher.signals import Signals


class Speech(object):

    def __init__(self):
        dispatcher.connect(self._handle_request, signal=Signals.SPEECH_MESSAGE, sender=dispatcher.Any)
       
        self.speechProg = os.environ['SPEECH_SCRIPT']
        
        self._run()

    def _handle_request(self, msg=None):
        subprocess.call([self.speechProg, msg])

    def _run(self):
        while True:
            time.sleep(10)


