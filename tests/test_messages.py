import pytest
from src.message import IRCClientMessage


def test_generate_simple_nick():
    # Message looks like: NICK foo
    msg = "NICK foo\r\n"
    assert IRCClientMessage("NICK", "foo").get_message() == msg


def test_generate_simple_user():
    # Message looks like: USER foo * * :PersonFoo Bar
    msg = "USER foo * * :PersonFoo Bar\r\n"
    assert (
        IRCClientMessage(
            "USER", "foo", "*", "*", ":PersonFoo Bar"
        ).get_message()
        == msg
    )
