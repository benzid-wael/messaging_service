# -*- coding: utf-8 -*-

class BaseHandler(object):
    """ All message handler should extend BaseHandler class. """

    message_type = None

    def __init__(self, filter_class

    def accept(self, message):
        return message['type'] == self.message_type

    def emit(self, record):
        raise NotImplementedError(".emit() should be overridden")
