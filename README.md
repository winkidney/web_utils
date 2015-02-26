Web Utils
------------

Web development utils classes and functions.
Current status: Under development and works in my project.
Find me in http://github.com/winkidney/web_utils.

Summaries are listed below.Documents will be written later.

##Install
```
pip install "web_utils[forms,security,sqlalchemy]" # to install all requirements.
```

##Summaries

+ code_loader - load code from str or unicode object and save it to cache or database
+ forms - some custom validator for wtfomrs
+ json_form - wrapper for jsonschema to validate json string like wtfomrs.
+ Security - password generator by bcrypt.Simple url sign generator.
+ _sqlalchemy - DBFieldConverter for convert alchemy's model instance to dict like string with white list support.
+ _pyramid - tools form pyramid web framework
+ extra - some other utils.


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

##web_utils.forms
WTFroms's custom field and other validator

+ validators
  + uuid_validator
  + TimeAfterNow  validator - return `True` if current datetime-field later than now.
  + MobilePhone validataor - Check if a number sequence is china's phone number
+ custom field
  + UnixTimeField
  + TextArrayField - convert `list` like `a, b, c ,1 ,3 ,3` to python list.
  + JsonField - Check if the text is json format string and convert it into python data(with `json.loads`)
  + IntArrayField - Convert list like `1,2,3,4,5` into python list(consists of python's `int` object)
+ utils
  + json2form - convert python dict into `MultiDict` which can be read by wtforms.

##web_utils.json_forms
Validate json string or dict object in wtforms's way.
Just inherit `JsonForm` class and call `validate` method to do validation.
Validation by `JsonSchema` , [Validation Quick Start](http://json-schema.org/latest/json-schema-validation.html).
Example listed below:
```python
class TestJsonForm(unittest.TestCase):
    class NewPMSSchema(JsonForm):
        schema = {
            "type": "object",
            "properties": {
                "to_uid": {
                    "type": "number",
                },
                "content": {
                    "type": "string",
                },
                "test": {
                    "type": "object",
                    "properties": {
                        "test1": {
                            "type": "integer",
                        }
                    }
                },
            },
            "required": ['to_uid', 'content'],
        }

form = TestJsonForm({'to_uid': 'a', 'content': 1})
# result
result = form.validate()
# errors
if not result:
    print form.errors
```

##web_utils.security
Not recommend to use it.

##web_utils._sqlalchemy
A sqlalchemy model to json data converter with white list and custom converter support.

###DBFCMixin
Just inherit it in your sqlalchemy model and call `as_dict` method to output python dict.
`class._default_output` is required.
Example listed below:

```python
class APIStorage(Base, DBFCMixin, StorageBackendMixin):

    __tablename__ = "api_storage"
    # white list
    _default_output = ('id', 'category', 'resource_name', 'document')

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Text, nullable=False)
    resource_name = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    ctime = Column(DateTime, default=datetime.datetime.utcnow)

# call as_dict method
model_instance = dbsession.query(APIStorage).first()
model_instance.as_dict(pure=False)  #False is default , with white list support.

```

###DBFieldConverter
Low level API for DBFCMixin
Quick example:

```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class APIStorage(Base):

    __tablename__ = "api_storage"
    _default_output = ('id', 'category', 'resource_name', 'document')

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Text, nullable=False)
    resource_name = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    ctime = Column(DateTime, default=datetime.datetime.utcnow)

# convert and output

model_instance = dbsession.query(APIStorage).first()

converter = DBFC(model_instance, model_instance._default_output)

converter.as_dict()

# as list
converter.as_list()

# without white list(output all data field)
converter.as_dict(pure=True)
```

####Register a Converter
DBFieldConverter supports Converter by sqlalchemy's field type.
```python
from sqlalchemy import Text
DBFieldConverter.register(Text)
```
will register Text type in DBFC.
  Note: without registered, DBFieldConverter will print `warning` information in console.

```python
DBFieldConverter.register(Text, lambda x:x[-1])
```
will output the last char of the input field which type is `Text`.

You can also pass `registry` to DBFieldConverter `__init__` method to specify `field type converter`.
For example:
```python
from sqlalchemy import Text
converter = DBFC(model_instance, model_instance._default_output, registry={Text: lambda x: x[-1]})
```
**Note:**  This registry will not overwrite other converter of DBFC's instance since it's `instance registry`.
Otherwise, `DBFC.registry` register class converter in it's registry.

###form2model
Easy set `wtfomrs` `Form` data to sqlalchemy's model field, name by name.

```python
form2model(form, model_instance, exclude=None)
```


##web_utils.extra
Some utils about argument parse ,datetime format.
+ GetSingleArgument    
  + bool(cls, value, default=False) default value support, will not return None.
  + integer(cls, value, default, nmin=None, nmax=None) - parse integer from string, return default value if not in given range.
  + string(cls, value, default='') - default value support
+ format_timestamp    
  from tornado core, to format timestamp
  ```python
  >>> format_timestamp(1359312200)
    'Sun, 27 Jan 2013 18:43:20 GMT'
  ```
+ AttrDict    
  Simple wrapper for `attr dict`     
  ```
  d = AttrDict({'a': 1})
  d.a # output 1
  ```    
  Many problem when use it, pay attention before you really know what you are doing.

