# coding: utf-8
import jsonschema


class JsonForm(object):

    schema = {}

    def __init__(self, data):
        if not hasattr(data, '__getitem__'):
            raise TypeError('')
        self.data = self._filter_data(data)
        self.errors = None

    def validate(self):
        try:
            jsonschema.validate(self.data, self.schema)
            return True
        except jsonschema.ValidationError as e:
            self.errors = str(e)
            return False

    def _filter_data(self, data):
        # todo : Add recursion support
        output = {}
        for key in data:
            if key in self.schema['properties']:
                if self.schema['properties'][key]['type'] == 'object':
                    output[key] = {}
                    for child_key in data[key]:
                        if child_key in self.schema['properties'][key]['properties']:
                            output[key][child_key] = data[key][child_key]
                else:
                    output[key] = data[key]
        return output
