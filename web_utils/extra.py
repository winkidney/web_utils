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

    def __setattr__(self, name, value):
        self[name] = value


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


class GetSingleArgument(object):

    _support_type = {
        'bool': None,
        'integer': None,
        'string': None,
    }

    @classmethod
    def get_single_argument(cls, value, arg_type, default, **kwargs):
        if arg_type not in cls._support_type:
            raise TypeError('arg_type `%s` not supported yet.' % arg_type)
        if arg_type == 'integer':
            result = cls._get_integer(value, **kwargs)
        elif arg_type == 'bool':
            result = cls._get_bool(value, **kwargs)
        elif arg_type == 'string':
            result = cls._get_string(value, **kwargs)
        else:
            result = None
        if result is None:
            return default
        return result

    @classmethod
    def bool(cls, value, default=False):
        return cls.get_single_argument(value, 'bool', default)

    @classmethod
    def integer(cls, value, default, nmin=None, nmax=None):
        return cls.get_single_argument(value, 'integer', default, nmin=nmin, nmax=nmax)

    @classmethod
    def string(cls, value, default=''):
        return cls.get_single_argument(value, 'string', default)

    @classmethod
    def _get_string(cls, input_value, **kwargs):
        return input_value

    @classmethod
    def _get_bool(cls, input_value, **kwargs):
        """
        Convert `0` `1` or `true` `false` string to python bool.
        :param input_value: a string that stands for bool
        :return: bool
        """
        if input_value is None:
            return None
        else:
            input_value = input_value.lower()
        if input_value in ['1', '0']:
            return bool(int(input_value))
        elif input_value in ['true', 'false']:
            if input_value == 'true':
                return True
            return False
        else:
            return None

    @classmethod
    def _get_integer(cls, input_value, nmin=None, nmax=None):
        """
        Use dict.get to access int value with max limit.
        If min and max not given, min=0 and the function will return
        validate it by min.
        :param input_value: GET or POST dict.
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
        return None

GSA = GetSingleArgument
