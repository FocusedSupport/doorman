import threading
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "components/slack")))

from slackbot.bot import Bot

import components.devices.doorbell_monitor as dm
import components.devices.camera as cam
import components.devices.lock as lock
import components.slack.slack_sender as ss
import components.slack.message_builder as mb
import components.slack.user_manager as um


def main():
    start_device_processing()
    start_slack_processing()


def start_device_processing():
    monitor = threading.Thread(target=dm.DoorbellMonitor)
    print("Starting doorbell monitor")
    monitor.start()

    camera = threading.Thread(target=cam.Camera)
    print("Starting camera")
    camera.start()

    lock_control = threading.Thread(target=lock.Lock)
    print("Starting lock control")
    lock_control.start()


def start_slack_processing():
    sender = threading.Thread(target=ss.SlackSender)
    print("Starting Slack sender")
    sender.start()

    msg_builder = threading.Thread(target=mb.MessageBuilder)
    print("Starting Slack message builder")
    msg_builder.start()

    bot = Bot()
    print("Starting Slack bot")
    user_manager = um.UserManager()
    user_manager.set_users(bot._client.users)
    bot.run()


if __name__ == "__main__":
    main()