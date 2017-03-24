from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re

from pydispatch import dispatcher

@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply("sup?")

DEFAULT_DOOR = 'main'
DEFAULT_DURATION = '5'
SIGNAL = "unlock"
SENDER = "slackbot"

@respond_to('^open\s*(main|side|)\s*(\d*)$', re.IGNORECASE)
def open_door(message, door, duration):
    if not door:
        door = DEFAULT_DOOR
    if not duration:
        duration = DEFAULT_DURATION

    message.reply("opening " + door + " for " + duration + " seconds")
    dispatcher.send(signal=SIGNAL, sender=SENDER, door=door, duration=duration, userid=message._get_user_id())