Web Utils
------------

Web development utils classes and functions.
Summaries are listed below.

+ code_loader
+ Validation
+ Security
+ __init__
+ pyramid
+ sqlalchemy



##web_utils.code_loader
Create a Codeloader instance to load and save code from Storage or str object.
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
  