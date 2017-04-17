import threading
import sys
import os
import signal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "components/slack")))

from slackbot.bot import Bot
from pydispatch import dispatcher
from components.dispatcher.signals import Signals, Senders

import components.devices.doorbell_monitor as dm
import components.devices.camera as cam
import components.devices.lock as lock
import components.devices.gpio_cleanup as gpio
import components.slack.slack_sender as ss
import components.slack.message_builder as mb
import components.slack.user_manager as um


def main():
    start_device_processing()
    start_slack_processing()


def start_device_processing():
    monitor = threading.Thread(target=dm.DoorbellMonitor)
    monitor.daemon = True
    print("Starting doorbell monitor")
    monitor.start()

    camera = threading.Thread(target=cam.Camera)
    camera.daemon = True
    print("Starting camera")
    camera.start()

    lock_control = threading.Thread(target=lock.Lock)
    lock_control.daemon = True
    print("Starting lock control")
    lock_control.start()

    gpio_cleanup = threading.Thread(target=gpio.GPIOCleanup)
    gpio_cleanup.daemon = True
    print("Starting GPIO cleanup module")
    gpio_cleanup.start()

def start_slack_processing():
    sender = threading.Thread(target=ss.SlackSender)
    sender.daemon = True
    print("Starting Slack sender")
    sender.start()

    msg_builder = threading.Thread(target=mb.MessageBuilder)
    msg_builder.daemon = True
    print("Starting Slack message builder")
    msg_builder.start()

    bot = Bot()
    print("Starting Slack bot")
    user_manager = um.UserManager()
    user_manager.set_users(bot._client.users)
    bot.run()

def cleanup():
    print("Caught interrupt...")
    dispatcher.send(Signals.CLEANUP, sender=Senders.SLACKBOT)
    dispatcher.send(Signals.EXIT, sender=Senders.SLACKBOT)
    exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cleanup()