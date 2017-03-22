import threading

from slackbot.bot import Bot

import components.doorbell.doorbell_monitor as dm
import components.slack.slack_sender as ss


def main():
    startDoorbellMonitor()
    startSlackSender()
    startBot()

def startBot():
    bot = Bot()
    print("Starting Slack bot")
    bot.run()

def startDoorbellMonitor():
    monitor = threading.Thread(target=dm.DoorbellMonitor)
    print("Starting doorbell monitor")
    monitor.start()

def startSlackSender():
    sender = threading.Thread(target=ss.SlackSender)
    print("Starting Slack sender")
    sender.start()

if __name__ == "__main__":
    main()