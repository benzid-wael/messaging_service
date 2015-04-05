# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import re


class BaseFilter(object):
    """ All message handler's filter should extend this class. """

    def filter(self, message):
        raise NotImplementedError(".filter() should be overridden")


class WindowTimeFilter(BaseFilter):

    """
    A message handler filter that filter out message received on the window time
    defined by `from_time` and `to_time`.
    """

    TIME_RE = re.compile(r'^(?P<hour>([0-9]|0[0-9]|1?[0-9]|2[0-3])):(?P<minute>[0-5]?[0-9])$')

    def __init__(self, from_time, to_time):
        self.from_time = from_time
        self.to_time = to_time

    def filter(self, record):
        now = datetime.now()
        from_dict = self.TIME_RE.match(self.from_time)
        to_dict = self.TIME_RE.match(self.to_time)
        from_hour = int(from_dict.groupdict()['hour'])
        from_minute = int(from_dict.groupdict()['minute'])
        to_hour = int(to_dict.groupdict()['hour'])
        to_minute = int(to_dict.groupdict()['minute'])
        from_day_diff = to_day_diff = 0
        if from_hour > to_hour:
            if (now.hour > from_hour
                    or (now.hour == from_hour and now.minute >= from_minute)):
                to_day_diff = 1
            else:
                from_day_diff = -1
        from_date = datetime(now.year, now.month, now.day + from_day_diff,
                             hour=from_hour,
                             minute=int(from_dict.groupdict()['minute']))
        to_date = datetime(now.year, now.month, now.day + to_day_diff,
                           hour=to_hour,
                           minute=int(from_dict.groupdict()['minute']))

        return not (from_date <= now <= to_date)
