# -*- coding: utf-8 -*-

import pytest
import socket
import smtplib

from service import settings

from service.handlers.email_handler import EmailHandler


class FakeEmailHandler(EmailHandler):

    def __init__(self, *args, **kwargs):
        super(FakeEmailHandler, self).__init__(*args, **kwargs)

    def sendmail(self, from_addr, to_addrs, msg, silent=True):
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

    def test_emit_just_text(self):
        record = {
            'type': 'email',
            'from': 'no-reply@company.com',
            'recipients': ['test1@test.com', 'test2@test.com'],
            'html': 'This is a test email. It can <i>also</i> contain HTML code',
            'text': 'This is a test email. It is text only'
        }
        result = self.handler.emit(record, include_html=False)
        expected = """Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
To: Recipient <test1@test.com,test2@test.com>
From: Author <no-reply@company.com>

This is a test email. It is text only"""
        assert result == expected

    def test_html_msg(self):
        record = {
            'type': 'email',
            'from': 'no-reply@company.com',
            'recipients': ['test1@test.com', 'test2@test.com'],
            'html': 'This is a test email. It can <i>also</i> contain HTML code',
            'text': 'This is a test email. It is text only'
        }
        result = self.handler.emit(record, include_html=True)
        expected_parts = (
            "Content-Type: multipart/alternative;",
            "To: Recipient <test1@test.com,test2@test.com>",
            "From: Author <no-reply@company.com>",
            "This is a test email. It is text only",
            "This is a test email. It can <i>also</i> contain HTML code",
        )
        for expected_part in expected_parts:
            assert expected_part in result


def test_success_emit():
    handler = EmailHandler(debuglevel=False)
    record = {
        'type': 'email',
        'from': 'no-reply@company.com',
        'recipients': ['test1@test.com', 'test2@test.com'],
        'html': 'This is a test email. It can <i>also</i> contain HTML code',
        'text': 'This is a test email. It is text only'
    }
    result = handler.emit(record, silent=False)
    assert result == None


def test_bad_host(monkeypatch):
    monkeypatch.setattr(settings, 'EMAIL_HOST', 'nohost.jrd.com')

    handler = EmailHandler(debuglevel=False)
    record = {
        'type': 'email',
        'from': 'no-reply@company.com',
        'recipients': ['test1@test.com', 'test2@test.com'],
        'html': 'This is a test email. It can <i>also</i> contain HTML code',
        'text': 'This is a test email. It is text only'
    }
    with pytest.raises(socket.gaierror):
        handler.emit(record, silent=False)


def test_bad_user(monkeypatch):
    monkeypatch.setattr(settings, 'EMAIL_HOST_USER', 'wael')

    handler = EmailHandler(debuglevel=False)
    record = {
        'type': 'email',
        'from': 'no-reply@company.com',
        'recipients': ['test1@test.com', 'test2@test.com'],
        'html': 'This is a test email. It can <i>also</i> contain HTML code',
        'text': 'This is a test email. It is text only'
    }
    with pytest.raises(smtplib.SMTPAuthenticationError):
        handler.emit(record, silent=False)
