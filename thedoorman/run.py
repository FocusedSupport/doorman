import threading

from slackbot.bot import Bot

import components.devices.doorbell_monitor as dm
import components.devices.camera as cam
import components.slack.slack_sender as ss
import components.slack.message_builder as mb


def main():
    start_device_processing()
    start_slack_processing()
    start_bot()


def start_bot():
    bot = Bot()
    print("Starting Slack bot")
    bot.run()


def start_device_processing():
    monitor = threading.Thread(target=dm.DoorbellMonitor)
    print("Starting doorbell monitor")
    monitor.start()

    camera = threading.Thread(target=cam.Camera)
    print("Starting camera")
    camera.start()


def start_slack_processing():
    sender = threading.Thread(target=ss.SlackSender)
    print("Starting Slack sender")
    sender.start()

    msg_builder = threading.Thread(target=mb.MessageBuilder)
    print("Starting Slack Message Builder")
    msg_builder.start()

if __name__ == "__main__":
    main()