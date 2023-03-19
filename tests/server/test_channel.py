from src.server.channel import Channel


def test_simple_channel_creation():
    channel = Channel("foo", "bar")

    assert channel.get_name() == "foo"
    assert channel.get_creator() == "bar"
    assert not channel.is_protected()


def test_protected_channel_creation():
    channel = Channel("foo", "bar", "password")

    assert channel.get_name() == "foo"
    assert channel.get_creator() == "bar"
    assert channel.is_protected()


def test_get_topic():
    channel = Channel("foo", "bar", "password")
    channel.set_topic("blah")

    assert channel.get_topic() == "blah"


def test_clear_topic():
    channel = Channel("foo", "bar", "password")
    channel.set_topic("blah")
    channel.clear_topic()

    assert not channel.get_topic()
