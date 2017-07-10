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

@respond_to('^say\s*(.*)$', re.IGNORECASE)
def say(message, whatToSay):
    username = UserManager().get_username(message._get_user_id())
    print("Got request to say a message from " + username + ": " + whatToSay)
    message.reply("Will say " + whatToSay)
    dispatcher.send(signal=Signals.SLACK_MESSAGE, sender=Senders.SLACKBOT, msg=whatToSay, suppressIconAndTime=True)

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