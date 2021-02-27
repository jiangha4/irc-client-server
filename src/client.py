import socket
import argparse
import time
from message import IRCClientMessage

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 42069        # The port used by the server

COMMAND_NICK = "NICK"
COMMAND_USER = "USER"
COMMAND_JOIN = "JOIN"


def arg_parser():
    parser = argparse.ArgumentParser(description='Client for simple IRC server')
    parser.add_argument('--nickname', '-n', type=str, required=True,
                        help='Nick name to use in the IRC Server')
    parser.add_argument('--username', '-u', type=str, required=True,
                        help='User name for the IRC Server')
    parser.add_argument('--fullname', '-f', type=str, required=True,
                        help='Real name for the IRC Server')

    return parser


class Client:
    def __init__(self, nickname, username, fullname, host, port):
        self.nickname = nickname
        self.username = username
        self.fullname = fullname
        self.host = host
        self.port = port
        self.conn = None

    def generate_nick_message(self):
        return IRCClientMessage(COMMAND_NICK, self.nickname).get_message()

    def generate_user_message(self):
        return IRCClientMessage(COMMAND_USER, self.username, "*", "*", ":" + self.fullname).get_message()

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))

        # Once connected with the server. Send NICK message
        nickname_message = self.generate_nick_message()
        self.send(nickname_message)
        time.sleep(1)
        username_message = self.generate_user_message()
        self.send(username_message)

    def listen(self):
        return self.conn.recv(512).decode('ascii')

    def send(self, message):
        self.conn.sendall(bytes(message, encoding='ascii'))


if __name__ == "__main__":
    args = arg_parser().parse_args()
    c = Client(args.nickname, args.username, args.fullname, HOST, PORT)
    c.connect()
    while True:
        msg = c.listen()
        if msg:
            print(msg)
