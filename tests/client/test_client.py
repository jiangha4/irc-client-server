from client.client import IRCClientMessage, Client


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


def test_client_generate_nick():
    c = Client("foo", "bar", "foo bar", None, None)

    expected = IRCClientMessage("NICK", "foo").get_message()
    actual = c.generate_nick_message()
    assert expected == actual


def test_client_generate_user():
    c = Client("foo", "bar", "foo bar", None, None)

    expected = IRCClientMessage(
        "USER", "bar", "*", "*", ":foo bar"
    ).get_message()
    actual = c.generate_user_message()

    assert expected == actual
