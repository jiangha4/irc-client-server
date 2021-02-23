from handler import handle_message
from message import parse_message

class User(object):
    def __init__(self, conn, host):
        self.registered = False
        self.alive = True
        self.host = host
        self.conn = conn

        self.nickname = None
        self.username = None

    def send(self, message):
        self.conn.sendall(bytes(message, encoding='ascii'))

    def get_response(self):
        return self.conn.recv(512).decode('ascii')

    def listen(self, server):
        while self.alive:
            try:
                raw_message = self.get_response()
                message = parse_message(raw_message)
                handle_message(self, message, server)
            except Exception as e:
                print(e)
                self.quit()

    def is_registered(self):
        return self.registered

    def register(self):
        if self.nickname and self.username:
            self.registered = True

    def set_nickname(self, nickname):
        self.nickname = nickname

    def set_username(self, username):
        self.username = username

    def quit(self):
        print("Exiting...")
        self.alive = False
