from src.server.user import User


def test_simple_user_creation():
    u = User("foo", "bar")

    assert u.alive
    assert not u.registered


def test_user_registration():
    u = User("foo", "bar")
    u.set_nickname("blah")
    u.register("w", "username", "fullname")

    assert u.is_registered()


def test_user_quit():
    u = User("foo", "bar")
    u.quit()

    assert not u.alive
