import socket
import argparse
import time
import re
import threading

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8888  # The port used by the server

COMMAND_NICK = "NICK"
COMMAND_USER = "USER"
COMMAND_JOIN = "JOIN"
COMMAND_PART = "PART"
WHITESPACE_CHAR = " "


class IRCClientMessage(object):
    """Standard IRC message from a client"""

    def __init__(self, command, *command_params):
        self.command = command
        self.command_params = [command]
        for param in command_params:
            self.command_params.append(param)
        self.message = self.generate_message()

    def generate_message(self):
        return WHITESPACE_CHAR.join(self.command_params) + "\r\n"

    def get_message(self):
        return str(self.message)


def arg_parser():
    parser = argparse.ArgumentParser(
        description="Client for simple IRC server"
    )
    parser.add_argument(
        "--nickname",
        "-n",
        type=str,
        required=True,
        help="Nick name to use in the IRC Server",
    )
    parser.add_argument(
        "--username",
        "-u",
        type=str,
        required=True,
        help="User name for the IRC Server",
    )
    parser.add_argument(
        "--fullname",
        "-f",
        type=str,
        required=True,
        help="Real name for the IRC Server",
    )

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
        return IRCClientMessage(
            COMMAND_USER, self.username, "*", "*", ":" + self.fullname
        ).get_message()

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))

        # Once connected with the server. Send NICK message
        nickname_message = self.generate_nick_message()
        print(nickname_message)
        self.send(nickname_message)
        time.sleep(1)
        username_message = self.generate_user_message()
        self.send(username_message)

    def listen(self):
        # TODO: Parse message and return text
        while True:
            message = self.conn.recv(512).decode("ascii")
            if message:
                print(message)

    def send(self, message):
        self.conn.sendall(bytes(message, encoding="ascii"))

    def process_msg(self, message):
        # Split once on the first white space occurrence
        try:
            msg_parts = message.split(" ", 1)
            targets = msg_parts[0]
            text = ":{}".format(msg_parts[1])
            valid_msg = "{} {}".format(targets, text)
            return valid_msg
        except Exception:
            return message


if __name__ == "__main__":
    args = arg_parser().parse_args()
    c = Client(args.nickname, args.username, args.fullname, HOST, PORT)
    c.connect()

    # start a listening thread
    threading.Thread(target=c.listen, daemon=True).start()

    alive = True
    while alive:
        user_input = input("> ")
        try:
            regex_cmd_match = re.match(r"^(\/\w+)(.*$)", user_input)
            user_cmd = regex_cmd_match.group(1).lower()
            user_cmd_params = regex_cmd_match.group(2).strip()

            if user_cmd == "/quit":
                parsed_msg = c.process_msg(user_cmd_params)
                msg_object = IRCClientMessage("QUIT", parsed_msg)
                c.send(msg_object.get_message())
                alive = False
            if user_cmd == "/nick":
                msg_object = IRCClientMessage("NICK", user_cmd_params)
            elif user_cmd == "/user":
                pass
            elif user_cmd == "/join":
                msg_object = IRCClientMessage("JOIN", user_cmd_params)
            elif user_cmd == "/privmsg":
                parsed_msg = c.process_msg(user_cmd_params)
                msg_object = IRCClientMessage("PRIVMSG", parsed_msg)
            elif user_cmd == "/part":
                parsed_msg = c.process_msg(user_cmd_params)
                msg_object = IRCClientMessage("PART", parsed_msg)
            elif user_cmd == "/list":
                msg_object = IRCClientMessage("LIST", user_cmd_params)
            elif user_cmd == "/names":
                msg_object = IRCClientMessage("NAMES", user_cmd_params)
            elif user_cmd == "/topic":
                parsed_msg = c.process_msg(user_cmd_params)
                msg_object = IRCClientMessage("TOPIC", parsed_msg)
            else:
                # TODO: unknown command prompt?
                pass
            c.send(msg_object.get_message())
        except Exception as e:
            pass
