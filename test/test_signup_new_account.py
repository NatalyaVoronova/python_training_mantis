import random
import string

def random_username(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join([random.choice(symbols) for _ in range(random.randrange(maxlen))])


def test_signup_new_account(app):
    username = random_username("user_", 10)
    email = username + "@localhost"
    password = "test"
    app.james.ensure_user_exist(username, password)
    app.signup.new_user(username, email, password)
    app.session.login(username, password)
    assert app.session.is_logged_in_as(username)
    app.session.logout()

def test_signup_new_account_soap(app):
    username = random_username("user_", 10)
    email = username + "@localhost"
    password = "test"
    app.james.ensure_user_exist(username, password)
    app.signup.new_user(username, email, password)
    assert app.soap.can_login(username, password)
