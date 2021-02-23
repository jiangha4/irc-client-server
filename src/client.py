import socket
from src.message import IRCMessage

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 42069        # The port used by the server

class Client:
    def __init__(self, nickname, username, fullname, host, port):
        self.nickname = nickname
        self.username = username
        self.fullname = fullname
        self.host = host
        self.port = port
        self.conn = None

    def generate_nick_message(self):
        prefix = None
        command = "NICK"
        command_params = self.nickname
        irc_nick_message = IRCMessage(prefix, command, command_params)

        return irc_nick_message.generate_message()

    def generate_user_message(self):
        prefix = None
        command = "USER"
        command_params = ['*', '*', ':' + self.username]

        irc_user_message = IRCMessage(prefix, command, command_params)

        return irc_user_message.generate_message()

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))

        # Once connected with the server. Send NICK message
        message = self.generate_nick_message()
        encoded_message = bytes(message, encoding='ascii')
        self.conn.sendall(encoded_message)
        self.conn.sendall(bytes(self.generate_user_message(), encoding='ascii'))

    def listen(self):
        return self.conn.recv(512).decode('ascii')

    def send(self, message):
        self.conn.sendall(bytes(message, encoding='ascii'))


if __name__ == "__main__":
    c = Client("m1ntyfresh", "jiangha4", "David Jiang", HOST, PORT)
    c.connect()
    while True:
        msg = c.listen()
        if msg:
            print(msg)
