# coding: utf-8

import json
import logging
import time
from sqlalchemy import Text, String, DateTime, Integer, Boolean, CHAR

__all__ = (
    'datetime2utmp',
    'form2model',
    'DBFC',
    'AlchemyJsonMixin'
)


def _list2unicode(the_list):
    """
    Return str if the input is a list or a tuple, else return itself.
    :param the_list: list or tuple
    :rtype: str or unicode
    """
    if isinstance(the_list, (list, tuple)):
        return ','.join((unicode(i) for i in the_list))
    return the_list


def datetime2utmp(datetime_instance):
    """
    :type datetime_instance: datetime.datetime
    :return: int
    """
    return int(time.mktime(datetime_instance.timetuple()))


def form2model(form, model_instance, exclude=None):
    """
    Set sqlalchemy model's property to wtforms's field data.
    :param form: wtforms's Form object
    :type form: wtforms.Form
    :param model_instance: sqlalchemy's model instance.
    :param exclude: A list of exclude field's name.
    :type exclude: list for tuple
    """
    for field in form._fields:
        if field not in exclude:
            setattr(model_instance, field, getattr(form, field).data)


class DBFCMixin(object):
    """Mixin object for sqlalchemy orm, just inherit and call model_instance.as_dict or cls.to_dict"""

    _default_output = None

    @classmethod
    def to_dict(cls, model_instance, pure=False):
        if not cls._default_output:
            raise NotImplementedError("cls._default_output can not be None.")
        if model_instance is None:
            return None
        return DBFC(model_instance, cls._default_output).as_dict(pure)

    def as_dict(self, pure=False):
        return self.to_dict(self, pure)


class DBFieldConverter(object):
    """
    Convert specified SQLAlchemy model to output dict or other format.
    """
    __slots__ = ('_registry', 'dict', 'model', 'registry', '_allows')
    _registry = {}

    def __init__(self, model_instance, allow_output=tuple(), registry={}, extra_out=tuple()):
        """
        If registry is given, same method in this registry will overwrite that in class _registry.
        :param model_instance:
            SQLAlchemy model instance, inherit from declarative_base().
        :type allow_output: list or tuple
        :param registry: dict like {column_type: convert_function}
        :type registry: dict
        :param extra_out: extra output field(class property, not a database table field)
        :type extra_out: list or tuple
        """

        if not hasattr(model_instance, '__table__'):
            raise TypeError("model_instance must be instance of sqlalchemy's model")
        if not isinstance(allow_output, (list, tuple)):
            raise TypeError("allowed outputs [{allow_output}] must be list or tuple")
        if not isinstance(registry, dict):
            raise TypeError('argument registry `{registry}` must be a dict.'.format(registry=registry))
        if not isinstance(extra_out, (list, tuple)):
            raise TypeError('argument extra_out `{0}` must be a dict.'.format(extra_out))

        self.registry = registry

        self.model = model_instance
        self._allows = allow_output
        # todo: improve or change default operation when model_instance is None.
        self.dict = dict((col, self._convert(getattr(self.model, col), type(self.model.__table__.columns[col].type))) for col in self.model.__table__.columns.keys())
        for key in extra_out:
            self.dict[key] = getattr(model_instance, key)

    def as_dict(self, pure=False):
        if pure:
            return self.dict
        else:
            return dict((item for item in self.dict.items() if item[0] in self._allows))

    def as_list(self, pure=False):
        if pure:
            return self.dict.items()
        else:
            return (item for item in self.dict.items() if item[0] in self._allows)


    @classmethod
    def register(cls, data_type, convert_method=None):
        """
        Register a field type converter to FieldConverter.
        Pass convert_method param or use default convert_method.
        If the data_type existed, this will return default
        :type data_type: wtforms.fields.Field
        :type convert_method: callable
        :rtype :bool
        :return True if register action succeed, else False.
        """
        if not isinstance(data_type, type):
            raise TypeError('{data_type} must be instance of type'.format(data_type=data_type))
        if convert_method is not None:
            if not callable(convert_method):
                raise TypeError('{convert_method} must be callable'.format(convert_method=convert_method))
        else:
            convert_method = lambda field: field
        cls._registry[data_type] = convert_method
        return True

    @classmethod
    def unregister(cls, data_type):
        """
        Unregister a data-type converter fucntion.
        :type data_type: type
        :rtype bool
        :return True if register successfully
        """
        if not isinstance(data_type, type):
            raise TypeError('{data_type} must be instance of type'.format(data_type=data_type))
        if cls._registry.get(data_type, None) is None:
            logging.warning("Type {data_type} does not exist in registry.".format(data_type=data_type))
        else:
            del cls._registry[data_type]
            return True

    def _convert(self, data, data_type):
        if data is None:
            return None
        if self.registry.get(data_type) is not None:
            return self.registry[data_type](data)
        elif self._registry.get(data_type) is not None:
            return self._registry[data_type](data)
        else:
            logging.warning('{type} not contained in registry, return its default value'.format(type=data_type))
            return data

try:
    from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID, INET
    DBFieldConverter.register(ARRAY, _list2unicode)
    DBFieldConverter.register(JSON, json.dumps)
    DBFieldConverter.register(UUID)
    DBFieldConverter.register(INET)
except ImportError:
    pass


DBFieldConverter.register(Text)
DBFieldConverter.register(String)
DBFieldConverter.register(DateTime, datetime2utmp)
DBFieldConverter.register(Integer)
DBFieldConverter.register(CHAR)
DBFieldConverter.register(Boolean)


DBFC = DBFieldConverter
