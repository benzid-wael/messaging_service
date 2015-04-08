# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import smtplib
import email.utils

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

    def emit(self, record, silent=True, include_html=True):
        subject = record.get('subject', 'Notification')
        from_addr = record['from']
        to_addrs = record['recipients']
        html_record = include_html and record['html']
        body = self.prepare(subject, from_addr, to_addrs, record['text'],
                            html_record)
        self.sendmail(from_addr, to_addrs, body, silent)
        if self.test:
            return body

    def prepare(self, subject, from_addr, recipients, text, html=None):
        if html:
            msg = MIMEMultipart('alternative')
            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            msg.attach(part2)
        else:
            msg = MIMEText(text)

        msg['To'] = email.utils.formataddr(('Recipient', ','.join(recipients)))
        msg['From'] = email.utils.formataddr(('Author', from_addr))
        return msg.as_string()

    def sendmail(self, from_addr, to_addrs, msg, silent=True):
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        try:
            server.set_debuglevel(self.debuglevel)

            # identify ourselves, prompting server for supported features
            server.ehlo()

            # If we can encrypt this session, do it
            if server.has_extn('STARTTLS'):
                server.starttls()
                server.ehlo()  # re-identify ourselves over TLS connection

            server.login(
                settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(from_addr, to_addrs, msg)
        except Exception as e:
            if not silent:
                raise e
        finally:
            server.quit()
