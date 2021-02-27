import socket
import threading
from src.user import User

class Server(object):
    RPL_WELCOME_TEMPLATE = "Welcome to the Internet Relay Network %s!%s@%s"

    def __init__(self):
        self.hostname = "127.0.0.1"
        self.port = 42069
        self.channels = {}
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
            threading.Thread(target=user.listen, args=(self,)).start()

    def get_user(self, userNickname):
        """Attempt to find the input nickname in the list of Users.
            If we can't find the user, return None"""
        for usr in self.users:
            if userNickname == usr.nickname:
                return usr
        return None
