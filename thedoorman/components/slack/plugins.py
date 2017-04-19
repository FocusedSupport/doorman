from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import time

from pydispatch import dispatcher
from components.dispatcher.signals import Signals, Senders
from components.slack.user_manager import UserManager

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
    dispatcher.send(signal=Signals.UNLOCK, sender=Senders.SLACKBOT, door=door, duration=duration, userid=message._get_user_id())



@respond_to('^picture$', re.IGNORECASE)
def request_picture(message):
    username = UserManager().get_username(message._get_user_id())
    message.reply("Taking a picture for " + username)
    print("Got slackbot picture command from " + username + " at time  %f" % time.time())
    dispatcher.send(signal=Signals.PICTURE_REQUEST, sender=Senders.SLACKBOT, username=username)