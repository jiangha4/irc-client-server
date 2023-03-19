import pytest
from src.server.message import parse_message, IRCMessage, BadMessageException


def test_parse_message_nick_phrase():
    msg = "NICK foo\r\n"

    actual = parse_message(msg)
    expected = IRCMessage(None, "NICK", ["foo"])

    assert actual.get_prefix() == expected.get_prefix()
    assert actual.get_command() == expected.get_command()
    assert actual.get_command_params() == expected.get_command_params()


def test_parse_message_user_phrase():
    msg = "USER foo * * :PersonFoo Bar\r\n"

    actual = parse_message(msg)
    expected = IRCMessage(None, "USER", ["foo", "*", "*", ":PersonFoo Bar"])

    assert actual.get_prefix() == expected.get_prefix()
    assert actual.get_command() == expected.get_command()
    assert actual.get_command_params() == expected.get_command_params()


def test_parse_message_bad_message():
    msg = "NICK bar"

    with pytest.raises(BadMessageException):
        parse_message(msg)


def test_parse_message_prefix_phrase():
    msg = ":127.0.0.1 JOIN #foobar\r\n"

    actual = parse_message(msg)
    expected = IRCMessage(":127.0.0.1", "JOIN", ["#foobar"])

    assert actual.get_prefix() == expected.get_prefix()
    assert actual.get_command() == expected.get_command()
    assert actual.get_command_params() == expected.get_command_params()
