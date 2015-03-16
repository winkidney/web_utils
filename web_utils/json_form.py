# coding: utf-8
import jsonschema
from jsonschema.validators import Draft4Validator


class JsonForm(object):

    schema = {}

    def __init__(self, json_data):
        if not hasattr(json_data, '__getitem__'):
            raise TypeError('json_data must be a dict.')
        if not self.schema:
            raise NotImplementedError('schema not implemented!')
        Draft4Validator.check_schema(self.schema)

        self.data = {}
        self._filter_data(json_data, self.schema['properties'], self.data)
        self.validator = Draft4Validator(self.schema)
        self.errors = None

    def validate(self):
        try:
            self.validator.validate(self.data, self.schema)
            return True
        except jsonschema.ValidationError as e:
            self.errors = str(e)
            return False

    def _filter_data(self, data, properties, output):
        for key in data:
            if key in properties:
                if properties[key]['type'].lower() == 'object':
                    output[key] = {}
                    self._filter_data(data[key], properties[key]['properties'], output[key])
                elif properties[key]['type'].lower() == 'number':
                    try:
                        output[key] = int(data[key])
                    except (ValueError, TypeError):
                        output[key] = data[key]
                elif properties[key]['type'].lower() == 'string':
                    try:
                        output[key] = str(data[key])
                    except UnicodeEncodeError:
                        output[key] = data[key]
                else:
                    output[key] = data[key]
