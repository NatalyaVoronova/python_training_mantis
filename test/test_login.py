

def test_login(app):
    if app.session.is_logged_in() is False:
        app.session.login("administrator", "root")
    assert app.session.is_logged_in_as("administrator")


