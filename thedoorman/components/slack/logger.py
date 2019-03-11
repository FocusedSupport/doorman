from pydispatch import dispatcher
from components.dispatcher.signals import Signals, Senders

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
        dispatcher.send(signal=Signals.LOG_MESSAGE, sender=Senders.SLACKBOT, msg=message)