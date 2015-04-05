# -*- coding: utf-8 -*-


class BaseFilter(object):
    """ All message handler's filter should extend this class. """

    def filter(self, message):
        raise NotImplementedError(".filter() should be overridden")
