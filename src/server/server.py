import socket
import threading
from user import User


class Server(object):
    def __init__(self):
        self.hostname = "0.0.0.0"
        self.port = 8888
        self.prefix = self.hostname
        self.channels = []
        self.users = []
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn.bind((self.hostname, self.port))

    def start(self):
        while True:
            # queue up to 5 connection requests
            self.conn.listen(5)
            # New client connection.
            clientsocket, (addr, port) = self.conn.accept()
            print("connected by", addr, port)
            user = User(clientsocket, addr)
            self.users.append(user)
            threading.Thread(target=user.listen, args=(self,)).start()

    def get_user(self, userNickname):
        """Attempt to find the input nickname in the list of Users.
        If we can't find the user, return None"""
        for usr in self.users:
            if userNickname == usr.nickname:
                return usr
        return None

    def is_nick_registered(self, nickname):
        """Attempt to find if a nickname is already registered to a user"""
        for user in self.users:
            if (nickname == user.get_nickname()) and (
                user.is_registered() and (user.alive)
            ):
                return True
        return False

    def get_prefix(self):
        return self.prefix

    def does_channel_exist(self, channel_name):
        for channel in self.channels:
            if channel_name == channel.get_name():
                return True
        return False

    def add_channel(self, channel):
        self.channels.append(channel)

    def get_channel(self, name):
        for channel in self.channels:
            if channel.get_name() == name:
                return channel
        return None

    def get_all_channels(self):
        return self.channels

    def get_public_channels(self):
        public_channels = []
        for channel in self.channels:
            if not channel.is_protected():
                public_channels.append(channel)
        return public_channels

    def get_private_channels(self):
        private_channels = []
        for channel in self.channels:
            if channel.is_protected():
                private_channels.append(channel)
        return private_channels
