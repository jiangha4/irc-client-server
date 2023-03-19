"""Runs the server"""
from server import Server  # pylint: disable=E0611

if __name__ == "__main__":
    s = Server()  # pylint: disable=E1102
    s.start()
