# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import smtplib
import email.utils

from email.mime.text import MIMEText

from service import settings

from .base import BaseHandler


class ConsoleHandler(BaseHandler):

    def emit(self, record):
        print("-> Email message %r sended to %s" % (
            record['text'], record['recipients']), file=sys.stdout)


class EmailHandler(BaseHandler):

    """ Email message handler. """

    def __init__(self, debuglevel=None, test=False):
        self.debuglevel = debuglevel or settings.DEBUG
        self.test = test

    def emit(self, record):
        subject = record.get('subject', 'Notification')
        from_addr = record['from']
        to_addrs = record['recipients']
        body = self.prepare(subject, from_addr, to_addrs, record['text'])
        self.sendmail(from_addr, to_addrs, body)
        if self.test:
            return body

    def prepare(self, subject, from_addr, recipients, msg):
        msg = MIMEText(msg)
        msg['To'] = email.utils.formataddr(('Recipient', ','.join(recipients)))
        msg['From'] = email.utils.formataddr(('Author', from_addr))
        return msg.as_string()

    def sendmail(self, from_addr, to_addrs, msg):
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        try:
            server.set_debuglevel(self.debuglevel)

            # identify ourselves, prompting server for supported features
            server.ehlo()

            # If we can encrypt this session, do it
            if server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo() # re-identify ourselves over TLS connection

            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(from_addr, to_addrs, msg)
        except Exception as e:
            if not silent:
                raise e
        finally:
            server.quit()
