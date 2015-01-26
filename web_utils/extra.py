# -*- coding:utf-8 -*-
import calendar
import email
import numbers
import time
import datetime

__author__ = 'winkidney'

__all__ = (
    'AttrDict',
    'format_timestamp',
)


class AttrDict(dict):
    #  __getattr__ todo IMPROVE
    def __init__(self, iterable, **kwargs):
        super(AttrDict, self).__init__(iterable, **kwargs)

    def __getattr__(self, item):
        return self[item]


def format_timestamp(ts):
    """Formats a timestamp in the format used by HTTP.

    The argument may be a numeric timestamp as returned by `time.time`,
    a time tuple as returned by `time.gmtime`, or a `datetime.datetime`
    object.

    >>> format_timestamp(1359312200)
    'Sun, 27 Jan 2013 18:43:20 GMT'
    """
    if isinstance(ts, numbers.Real):
        pass
    elif isinstance(ts, (tuple, time.struct_time)):
        ts = calendar.timegm(ts)
    elif isinstance(ts, datetime.datetime):
        ts = calendar.timegm(ts.utctimetuple())
    else:
        raise TypeError("unknown timestamp type: %r" % ts)
    return email.utils.formatdate(ts, usegmt=True)
