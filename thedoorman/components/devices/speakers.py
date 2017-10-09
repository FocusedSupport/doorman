import os
import time
import pygame
import urllib.request
import subprocess
import re

from pydispatch import dispatcher
from ..dispatcher.signals import Signals


class Speakers(object):

    def __init__(self):
        dispatcher.connect(self._handle_doorbell, signal=Signals.DOORBELL, sender=dispatcher.Any)
        dispatcher.connect(self._handle_request, signal=Signals.AUDIO_REQUEST, sender=dispatcher.Any)
        dispatcher.connect(self._cancel_playback, signal=Signals.AUDIO_CANCEL, sender=dispatcher.Any)
       
        pygame.mixer.init()
        self.doorbell_sound = os.environ['DOORBELL_SOUND']
        self.ytdl = os.environ['YOUTUBEDL_PATH']
        self.tmpDir = "/tmp/"

        self._run()

    def _handle_doorbell(self):
        self._play_sound(self.doorbell_sound)

    def _handle_request(self, url):
        if re.match(".*youtu\.?be.*", url) != None:
            sound_file = self._download_youtube(url)
        else:
            sound_file = self._download_url(url)
        if sound_file != None:
            self._play_sound(sound_file)

    def _download_url(self, url):
        sound_file = self.tmpDir + os.path.basename(url)
        urllib.request.urlretrieve(url, sound_file)
        return sound_file

    def _download_youtube(self, url):
        outputpath = self.tmpDir + "%(id)s.%(ext)s"
        pattern = ".*Destination: " + self.tmpDir + "(\w+\.mp3).*"
        regexp = re.compile(pattern)

        url = url.strip("<>")
        proc = subprocess.Popen(
            [self.ytdl, '-o', outputpath, '-f', 'mp3/bestaudio', '-x', '--audio-format', 'mp3', url],
            stdout=subprocess.PIPE)
        audioFile = None
        for line in proc.stdout:
            strLine = line.decode('utf-8')
            result = regexp.match(strLine)
            if result != None:
                audioFile = self.tmpDir + result.group(1)
        return audioFile

    def _run(self):
        while True:
            time.sleep(10)

    def _cancel_playback(self):
        pygame.mixer.music.stop()

    def _play_sound(self, sound_file):
        print("Speakers: playing ", sound_file)

        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy() == True:
            time.sleep(.25)
