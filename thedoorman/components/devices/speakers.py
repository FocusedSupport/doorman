import os
import time
import pygame

from pydispatch import dispatcher
from ..dispatcher.signals import Signals


class Speakers(object):

    def __init__(self):
        dispatcher.connect(self._handle_doorbell, signal=Signals.DOORBELL, sender=dispatcher.Any)
        #dispatcher.connect(self._handle_request, signal=Signals.SOUND_REQUEST, sender=dispatcher.Any)
       
        pygame.mixer.init()
        self.doorbell_sound = os.environ['DOORBELL_SOUND']
        
        self._run()

    def _handle_doorbell(self):
        self._play_sound(self.doorbell_sound)

    def _run(self):
        while True:
            time.sleep(10)

    def _play_sound(self, sound_file):
        print("Speakers: playing ", sound_file)
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() == True:
            time.sleep(.25)

