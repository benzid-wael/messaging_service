# -*- coding: utf-8 -*-

import pytest

from service.handlers import SMSHandler


def test_good_records(capsys):
    msg = {
        'type': 'sms',
        'from': 'JRD',
        'recipients': ['+971501478902'],
        'body': 'Test SMS message body',
    }
    expected = (
        "-> SMS message 'Test SMS message body' sended to ['+971501478902']\n"
    )
    handler = SMSHandler()
    handler.emit(msg)
    out, err = capsys.readouterr()
    assert err == expected


def test_bad_record():
    msg = {
        'type': 'sms',
    }
    handler = SMSHandler()
    with pytest.raises(KeyError):
        handler.emit(msg)
