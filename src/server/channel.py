"""This module models a channel object as described by RFC2812"""
class Channel(object):
    def __init__(self, name, creator, password=None):
        self.name = name
        self.users = []
        self.password = password
        self.topic = None
        self.creator = creator

    def add_user(self, nickname):
        """Add user object to users list"""
        self.users.append(nickname)

    def set_topic(self, topic):
        self.topic = topic

    def get_users(self):
        return self.users

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password

    def get_topic(self):
        return self.topic

    def clear_topic(self):
        self.topic = None

    def is_user_in_channel(self, nickname):
        for usr in self.users:
            if usr.get_nickname() == nickname:
                return True
        return False

    def remove_user(self, nickname):
        new_users = [
            user for user in self.users if user.get_nickname() != nickname
        ]
        self.users = new_users

    def is_protected(self):
        if self.password:
            return True
        return False

    def get_creator(self):
        return self.creator

    def set_creator(self, creator):
        self.creator = creator
