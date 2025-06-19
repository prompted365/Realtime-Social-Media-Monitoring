import email_sender


class DummySMTP:
    def __init__(self, *args, **kwargs):
        self.login_args = None
        self.sent_from = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def login(self, user, password):
        self.login_args = (user, password)

    def sendmail(self, from_addr, to_addr, msg):
        self.sent_from = from_addr


def test_send_email_uses_env(monkeypatch):
    smtp_instance = DummySMTP()
    monkeypatch.setenv("EMAIL_SENDER", "me@example.com")
    monkeypatch.setenv("EMAIL_PASSWORD", "secret")
    monkeypatch.setattr(email_sender.smtplib, "SMTP_SSL", lambda *a, **k: smtp_instance)
    email_sender.send_email([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "you@example.com", "brand")
    assert smtp_instance.login_args == ("me@example.com", "secret")
    assert smtp_instance.sent_from == "me@example.com"
