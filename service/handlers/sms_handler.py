# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

from .base import BaseHandler


class SMSHandler(BaseHandler):

    """ SMS message handler. This is a fake SMS handler it just print received
    messages to the attached stream (stderr by default). """

    def __init__(self, stream=None):
        self.stream = stream or sys.stderr

    def emit(self, record):
        print("-> SMS message %r sended to %s" % (
            record['body'], record['recipients']), file=self.stream)
