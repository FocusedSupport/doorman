from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import time
import netifaces

from datetime import timedelta
from pydispatch import dispatcher
from components.dispatcher.signals import Signals, Senders
from components.slack.user_manager import UserManager

@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply("sup?")

DEFAULT_DOOR = 'main'
DEFAULT_DURATION = '5'
MAX_DURATION = '300'

@respond_to('^\s*help\s*$', re.IGNORECASE)
def help_me(message):
    help_str = """I know the following commands:

    open [main|side] [duration]
 
        Unlocks the appropriate door for [duration] seconds.  Default
        door is the main door, default time is 5 seconds.  Max time is
        300 seconds.

    r
        Repeats the previous open command for this user.   History is not
        saved between restarts of the doorman bot.

    picture

        Take a picture as if the doorbell button was pressed, and post it
        to the channel.

    say (message)

        Repeats the message on to the channel.
        
    speak (message)
    
        Says the message over the speakers.    

    play (MP3 URL)

        Downloads and plays the MP3 audio designated by the provided URL.

    cancel audio

        Stops any currently running audio playback.

    how are you?

        Replies to the message with status information for the doorman.

    help

        Replies with this help message.


    All commands can be sent to the doorman in a private message, or 
    directed to the doorman in a mention (e.g.  @doorman how are you? in the
    channel will cause the reply to go to the channel)
"""
    message.reply('```' + help_str + '```')

@respond_to('^open\s*(main|side|)\s*(\d*)\s*$', re.IGNORECASE)
def open_door(message, door, duration):
    if not door:
        door = DEFAULT_DOOR
    if not duration:
        duration = DEFAULT_DURATION

    if float(duration) < 0:
        message.reply("Invalid duration " + duration + ", using " + DEFAULT_DURATION)
        duration = DEFAULT_DURATION
    if float(duration) > float(MAX_DURATION):
        message.reply("Invalid duration " + duration + ", using " + MAX_DURATION)
        duration = MAX_DURATION

    message.reply("opening " + door + " for " + duration + " seconds")
    dispatcher.send(signal=Signals.UNLOCK, sender=Senders.SLACKBOT, door=door, duration=duration, userid=message._get_user_id())

@respond_to('^\s*r\s*$', re.IGNORECASE)
def repeat_open(message):
    print("attempting to repeat previous unlock command")
    dispatcher.send(signal=Signals.UNLOCK_HISTORY, sender=Senders.SLACKBOT, message=message)

@respond_to('^picture$', re.IGNORECASE)
def request_picture(message):
    username = UserManager().get_username(message._get_user_id())
    message.reply("Taking a picture for " + username)
    print("Got slackbot picture command from " + username + " at time  %f" % time.time())
    dispatcher.send(signal=Signals.PICTURE_REQUEST, sender=Senders.SLACKBOT, username=username)

@respond_to('^say\s*(.*)$', re.IGNORECASE)
def say(message, whatToSay):
    username = UserManager().get_username(message._get_user_id())
    print("Got request to say a message from " + username + ": " + whatToSay)
    message.reply("Will say " + whatToSay)
    dispatcher.send(signal=Signals.SLACK_MESSAGE, sender=Senders.SLACKBOT, msg=whatToSay, suppressIconAndTime=True)

@respond_to('^speak\s*(.*)$', re.IGNORECASE)
def say(message, whatToSay):
    username = UserManager().get_username(message._get_user_id())
    print("Got request to speak a message from " + username + ": " + whatToSay)
    message.reply("Will speak " + whatToSay)
    dispatcher.send(signal=Signals.SPEECH_MESSAGE, sender=Senders.SLACKBOT, msg=whatToSay)

@respond_to('^play\s*(.*)$', re.IGNORECASE)
def play(message, audio_file):
    username = UserManager().get_username(message._get_user_id())
    print("Got request to play an audio file from " + username + ": " + audio_file)
    message.reply("Will play " + audio_file)
    dispatcher.send(signal=Signals.AUDIO_REQUEST, sender=Senders.SLACKBOT, file=audio_file)

@respond_to('^cancel audio.*$', re.IGNORECASE)
def cancel(message):
    username = UserManager().get_username(message._get_user_id())
    print("Got request to cancel audio playback from " + username)
    message.reply("Will cancel audio playback")
    dispatcher.send(signal=Signals.AUDIO_CANCEL, sender=Senders.SLACKBOT)

@respond_to('^how are you?', re.IGNORECASE)
def status(message):
    message.reply("I'm good, thanks.")
    message.reply("My system uptime is " + uptime() + ".")
    message.reply(ipAddrs())
    message.reply("My CPU temperature is " + cpuTemp() + ".")

def uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = int(float(f.readline().split()[0]))
        uptime_string = str(timedelta(seconds=uptime_seconds))
    return uptime_string

def ipAddrs():
    ifaces = netifaces.interfaces()
    validAddrs = []
    for ifaceName in ifaces:
        addrs = netifaces.ifaddresses(ifaceName).get(netifaces.AF_INET)
        if (addrs != None):
            addr = addrs[0].get('addr')
            if addr != '127.0.0.1':
                validAddrs.append(addr)
    if len(validAddrs) == 0:
        return "I don't seem to have an IP address.... strange!"
    elif len(validAddrs) == 1:
        return "My IP address is " + validAddrs[0] + "."
    else:
        return "My IP addresses are " + ", ".join(validAddrs) + "."


def cpuTemp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        tempString = f.read()
        tempC = float(tempString) / 1000
        tempF = round(float(1.8 * tempC) + 32, 1)
        return str(tempF) + u"\u00b0" + " F"
