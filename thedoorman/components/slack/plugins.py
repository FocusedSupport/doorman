from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re

from pydispatch import dispatcher
from components.dispatcher.signals import Signals, Senders

@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply("sup?")

DEFAULT_DOOR = 'main'
DEFAULT_DURATION = '5'

@respond_to('^open\s*(main|side|)\s*(\d*)$', re.IGNORECASE)
def open_door(message, door, duration):
    if not door:
        door = DEFAULT_DOOR
    if not duration:
        duration = DEFAULT_DURATION

    message.reply("opening " + door + " for " + duration + " seconds")
    dispatcher.send(signal=Signals.DOORBELL, sender=Senders.SLACKBOT, door=door, duration=duration, userid=message._get_user_id())



@respond_to('^picture$', re.IGNORECASE)
def request_picture(message):
    message.reply("Taking a picture")
    dispatcher.send(signal=Signals.PICTURE_REQUEST, sender=Senders.SLACKBOT)