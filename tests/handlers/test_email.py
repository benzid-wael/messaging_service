# -*- coding: utf-8 -*-

from service.handlers.email_handler import EmailHandler


class FakeEmailHandler(EmailHandler):

    def __init__(self, *args, **kwargs):
        super(FakeEmailHandler, self).__init__(*args, **kwargs)

    def sendmail(self, from_addr, to_addrs, msg):
        return 'OK'


class TestEmailHandler:

    @classmethod
    def setup_class(cls):
        cls.handler = FakeEmailHandler(debuglevel=False, test=True)

    def test_prepare(self):
        result = self.handler.prepare('', 'none@jrd.com',
                                      ['client@example.foo'], 'Just a test')
        expected = """Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
To: Recipient <client@example.foo>
From: Author <none@jrd.com>

Just a test"""
        assert result == expected

    def test_emit(self):
        record = {
            'type': 'email',
            'from': 'no-reply@company.com',
            'recipients': ['test1@test.com', 'test2@test.com'],
            'html': 'This is a test email. It can <i>also</i> contain HTML code',
            'text': 'This is a test email. It is text only'
        }
        result = self.handler.emit(record)
        expected = """Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
To: Recipient <test1@test.com,test2@test.com>
From: Author <no-reply@company.com>

This is a test email. It is text only"""
        assert result == expected
