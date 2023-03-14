from src.handler import handle_message
from src.message import parse_message


class User(object):
    def __init__(self, conn, host):
        self.registered = False
        self.alive = True
        self.host = host
        self.conn = conn

        self.mode = None
        self.nickname = None
        self.username = None
        self.fullname = None

    def send(self, message):
        self.conn.sendall(bytes(message, encoding="ascii"))

    def get_response(self):
        return self.conn.recv(512).decode("ascii")

    def listen(self, server):
        while self.alive:
            # try:
            raw_message = self.get_response()
            if raw_message:
                irc_message = parse_message(raw_message)
                handle_message(self, server, irc_message)
        # except Exception as e:
        #    print(e)
        #    self.quit()

    def is_registered(self):
        return self.registered

    def register(self, mode, username, fullname):
        self.set_mode(mode)
        self.set_username(username)
        self.set_fullname(fullname)

        if self.nickname and self.username:
            self.registered = True

    def set_nickname(self, nickname):
        self.nickname = nickname

    def get_nickname(self):
        return self.nickname

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_fullname(self, fullname):
        self.fullname = fullname

    def get_fullname(self):
        return self.fullname

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        return self.mode

    def get_hostname(self):
        return self.host

    def quit(self):
        self.alive = False

    def __repr__(self):
        return self.get_nickname()
