def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return get_instance


@singleton
class UserManager(object):

    def __init__(self):
        self._count = 0
        self._users = {}

    def inc(self):
        self._count += 1

    def set_users(self, users):
        self._users = users

    def get_username(self, userid=None):
        user = self._users[userid]
        if user:
            return user['name']