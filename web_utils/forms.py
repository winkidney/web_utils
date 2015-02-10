# !/usr/bin/env python
# coding: utf-8
import json
import time
import datetime
try:
    from webob.multidict import MultiDict
except ImportError:
    MultiDict = dict
from wtforms import IntegerField, StringField
from wtforms.validators import ValidationError

__author__ = 'winkidney'

__doc__ = """
Validators and Field collection for wtfroms.
`GET` and `POST` parameters filter.
"""

__all__ = (
    'safe_int_arg',
    'uuid_validator',
    'TimeAfterNow',
    'MobilePhone',
    'TextArrayField',
    'UnixTimeField',
    'JsonField',
    'IntArrayField',
)


def uuid_validator(field):
    if isinstance(field, (str, unicode)) and \
            map(lambda s: len(s), field.split('-')) == [8, 4, 4, 4, 12]:
        return True
    else:
        return False


def utmp2datetime(unix_timestamp):
    """
    :type unix_timestamp: int or str
    :return: datetime.datetime
    """
    return datetime.datetime.fromtimestamp(unix_timestamp)


def datetime2utmp(datetime_instance):
    """
    :type datetime_instance: datetime.datetime
    :return: int
    """
    return int(time.mktime(datetime_instance.timetuple()))


### wtf custom validators ###
def TimeAfterNow(form, field):
    if field.data:
        if field.data < datetime.datetime.utcnow():
            raise ValidationError('This time field must later than now.')


def MobilePhone(form, field):
    if field.data.isdigit() and len(field.data) == 11:
        return
    raise ValidationError('Not valid mobile phone number')


class UnixTimeField(IntegerField):
    """
    UnixTimeField, except stores a `datetime.date`.
    """
    def _value(self):
        if self.raw_data:
            return int(time.mktime(self.raw_data.timetuple()))
        elif self.data is not None:
            return int(time.mktime(self.data.timetuple()))
        else:
            return None

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = utmp2datetime(int(valuelist[0]))
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid unix timestamp'))


class TextArrayField(StringField):
    """
    Except stores a `list` contains text, splited by `,`.
    """
    def _value(self):
        if self.raw_data:
            return ','.join(unicode(i) for i in self.raw_data[0])
        elif self.data is not None:
            return ','.join(unicode(i) for i in self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [i.strip() for i in valuelist[0].split(',') if i]
        else:
            self.data = []


class JsonField(StringField):
    """
    Except stores a `list` contains text, splited by `,`.
    """
    def _value(self):
        if self.raw_data:
            return json.dumps(self.raw_data[0])
        elif self.data is not None:
            return json.dumps(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                if valuelist[0] is not None:
                    self.data = json.loads(valuelist[0])
                else:
                    self.data = {}
            except ValueError:
                self.data = {}
                raise ValueError(self.gettext('Not a valid Json Strings'))


class IntArrayField(IntegerField):
    """
    Except stores a `list` contains integers, splited by `,`.
    """
    def _value(self):
        if self.raw_data:
            return ','.join(unicode(i) for i in self.raw_data[0])
        elif self.data is not None:
            return ','.join(unicode(i) for i in self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = [int(i.strip()) for i in valuelist[0].split(',') if i]
            except ValueError:
                self.data = []
                raise ValueError(self.gettext('Not a valid IntArray field, requires format like `1,2,3`.'))


class PyIntArrayField(StringField):
    """
    Warning: Just for MultiDict from a json_body from request.
    Except stores a python style `list` contains integers, split by `,` and wrapped by `[]`.
    """
    def _value(self):
        if self.raw_data:
            return ','.join(unicode(i) for i in self.raw_data[0])
        elif self.data is not None:
            return ','.join(unicode(i) for i in self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            if isinstance(valuelist[0], (list, tuple)):
                self.data = valuelist[0]
                for i in self.data:
                    if not isinstance(i, int):
                        raise ValueError(self.gettext('Not a valid IntArray field, requires format like `[1,2,3]`.'))
                return
            self.data = []
            raise ValueError('Not a valid IntArray field, requires format like `[1,2,3]`.')


def json2form(json_dict):
    """
    Warning:if webob.multidict.MultiDict does not exist, the dict object will be used.
    WTForms can not recognize dict but MultiDict works well.
    """
    form_dict = MultiDict()
    for item in json_dict.items():
        if item[1] is None:
            form_dict[item[0]] = ''
        else:
            form_dict[item[0]] = item[1]

    return form_dict