Web Utils
------------

Web development utils classes and functions.
Current status: Under development and works in my project.
Find me in http://github.com/winkidney/web_utils.

Summaries are listed below.Documents will be written later.

##Summaries

+ code_loader - load code from str or unicode object and save it to cache or database
+ forms - some custom validator for wtfomrs
+ json_form - wrapper for jsonschema to validate json string like wtfomrs.
+ Security - password generator by bcrypt.Simple url sign generator.
+ __init__ - some other utils.
+ _pyramid - tools form pyramid web framework
+ _sqlalchemy - DBFieldConverter for convert alchemy's model instance to dict like string with white list support.



##web_utils.code_loader

Create a Code loader instance to load and save code from Storage or str object.
Return a python module object that you can run any code within it.

+ Methods
  + __init__(name, storage_backend=DummyStorageBackend, cache_backend=DummyCacheBackend)
    Create a loader with given storage_backend and cache_backend.
  + create_module(fullname, code_script, save_key=None)
    if `save_key` is given, use it instead of fullname as `accees_key` passed to storage backend's `set` method.
  + save(mod, cached=False, **kwargs)
    save a module object into storage backend and cache backend(optional).
    **kwargs will be passed to backend's `set` method.
  + load(fullname, save_key=None, **kwargs)
    Load a module by its name(if `save_key` is given, use it instead).
  