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


def safe_int_arg(input_value, default=None, nmin=None, nmax=None):
    """
    Use dict.get to access int value with max limit.
    If min and max not given, min=0 and the function will return
    validate it by min.
    :param input_value: GET or POST dict.
    :param default: default returned value
    :param nmin: range limit of argument
    :param nmax: range limit of argument
    :return: if input_value is not valid, return will be `default`, not nmin or nmax.
    :rtype int
    """
    try:
        value = int(input_value)
        if nmax is not None and nmin is not None:
            if nmin <= value <= nmax:
                return value
        elif nmin is not None:
            if value >= nmin:
                return value
        elif nmax is not None:
            if value <= nmax:
                return value
        else:
            return value
    except (ValueError, TypeError):
        pass
    return default


def get_single_argument(arg_dict, name, default=None):
    try:
        return arg_dict[name]
    except KeyError:
        return default