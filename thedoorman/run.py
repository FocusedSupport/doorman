import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "bot")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "doorbell")))

from slackbot.bot import Bot
import doorbell.DoorbellMonitor as dm

def main():
    startDoorbellMonitor()
    startBot()

def startBot():
    bot = Bot()
    print("Starting Slack bot")
    bot.run()

def startDoorbellMonitor():
    monitor = dm.DoorbellMonitor()
    print("Starting doorbell monitor")
    monitor.run()

if __name__ == "__main__":
    main()