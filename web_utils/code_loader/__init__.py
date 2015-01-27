# coding: utf-8
from abc import ABCMeta, abstractmethod
import logging
import imp
import sys
import traceback
try:
    import cPickle as pickle
except ImportError:
    import pickle


logger = logging.getLogger("CodeLoader")

__all__ = (
    'StorageBackendMixin',
    'CacheBackendMixin',
    'CodeLoader',
)


class StorageBackendMixin(object):

        @classmethod
        @abstractmethod
        def sget(cls, key, **kwargs):
            pass

        @classmethod
        @abstractmethod
        def sset(cls, key, value, **kwargs):
            pass


class DummyStorageBackend(StorageBackendMixin):
    """
    Just a example, do not apply it to productive application.
    """

    _storage = {}

    @classmethod
    def sget(cls, key, **kwargs):
        return cls._storage.get(key)

    @classmethod
    def sset(cls, key, value, **kwargs):
        cls._storage[key] = value


class CacheBackendMixin(object):

    @classmethod
    @abstractmethod
    def cget(cls, key, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def cset(cls, key, value, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def cdelete(cls, key):
        pass


class DummyCacheBackend(CacheBackendMixin):
    """
    Just a example, do not apply it to productive application.
    """
    _cached = {}

    @classmethod
    def cget(cls, key, **kwargs):
        return cls._cached.get(key)

    @classmethod
    def cset(cls, key, value, **kwargs):
        cls._cached[key] = value

    @classmethod
    def cdelete(cls, key):
        if key in cls._cached:
            del cls._cached[key]


class CodeLoader(object):
    """
    Get a module object from script file or string.
    """

    def __init__(self, name, storage_backend=DummyStorageBackend, cache_backend=DummyCacheBackend):
        if not issubclass(storage_backend, StorageBackendMixin):
            raise TypeError("storage_backend must be subclass of StorageBackendMixin")
        if not issubclass(cache_backend, CacheBackendMixin):
            raise TypeError("cache_backend must be subclass of CacheBackendMixin")
        self.name = name
        self._cache_prefix = 'Loader_{cache_backend_name}_'.format(cache_backend_name=cache_backend.__name__)
        self._storage_backend = storage_backend
        self._cache_backend = cache_backend

    def create_module(self, fullname, code_script, save_key=None):
        """
        Create a module from object as a normal python module.
        if `save_key` is given, use it instead of fullname as `accees_key` passed to storage backend's `set` method.
        :param fullname: module name, will be joined with prefix `dynamic_loaded.`
        :param code_script: the utf-8 encoded bytes object(in python2, it is `str`)
        :param save_key: save key that will be used by storage_backend, You can also run 'CodeLoader.load(save_key)' to
            access the saved code object.
        :type fullname: str or unicode
        :type code_script: str
        :return: module object if success, return None if fail with anything wrong with the code's runtime error.
        """
        if not isinstance(code_script, (str, unicode)):
            raise TypeError("code_script param must instance of str")

        code = self._compile(fullname, code_script)
        if code is None:
            return None

        mod = imp.new_module(fullname)
        mod.__file__ = fullname
        mod.__loader__ = self
        mod.__package__ = ''
        mod.__script__ = code_script
        if save_key is None:
            mod.__save_key__ = fullname
        else:
            mod.__save_key__ = save_key

        try:
            exec(code, mod.__dict__)
            return mod
        except:
            exc_type, exc_value, traceback = sys.exc_info()
            logger.warning(
                "Bad codes, info listed below:\n"
                "exec_type: %s\n exec_value: %s\n traceback: %s" % (exc_type, exc_value, traceback)
            )
            return None

    def save(self, mod, cached=False, **kwargs):
        """
        Save mod's script to storage backend, is cached=True, cache_backend will be used or refreshed.
        **kwargs will be passed to backend's `set` method.
        """
        self._storage_backend.sset(mod.__save_key__, mod.__script__, **kwargs)
        if cached:
            self._cache_backend.cset(mod.__save_key__, pickle.dumps(mod), **kwargs)
        else:
            self._cache_backend.cdelete(mod.__save_key__)

    def load(self, fullname, save_key=None, **kwargs):
        """
        Load a module from storage backend or cache backend.
        **kwargs will be passed to backend's `set` method.
        :param fullname:
        :param save_key:
        :param kwargs:
        :return: loaded mod or None.
        """
        if save_key:
            access_key = save_key
        else:
            access_key = fullname
        result = self._cache_backend.cget(access_key)
        if result:
            return pickle.loads(result)
        else:
            result = self._storage_backend.sget(access_key, **kwargs)
            if result:
                return self.create_module(fullname, result, access_key)
            return None

    def _compile(self, fullname, code_script):
        """
        :type fullname: str or unicode
        :type code_script: str
        """
        try:
            return compile(code_script, fullname, 'exec')
        except SyntaxError:
            exc_type, exc_value, tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, tb)
            logger.warning("code script `%s` has SyntaxError:\n"
                           "The code:\n%s" % (fullname, code_script))
            return None