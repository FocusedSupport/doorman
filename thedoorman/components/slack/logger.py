from pydispatch import dispatcher
from components.dispatcher.signals import Signals, Senders
import time

def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance


@singleton
class Logger(object):

    def __init__(self):
        self._count = 0

    def log(self, message=None):
        formatted_time = time.strftime("%Y%m%d-%H%M%S")
        formatted_msg = "[" + formatted_time + "]: " + message
        print(formatted_msg)
        wrapped_msg = "`" + formatted_msg + "`"
        dispatcher.send(signal=Signals.LOG_MESSAGE, sender=Senders.SLACKBOT, msg=wrapped_msg)