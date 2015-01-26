# coding: utf-8
import unittest
from qadmin.utils.code_loader import CodeLoader

normal_code = """
import os
class TestClass(object):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

def test_function(name):
    return name
"""


class TestCodeLoader(unittest.TestCase):

    def setUp(self):
        self.syntax_error_code = "fuckme,,,,,,,,,"
        self.normal_code = normal_code
        self.runtime_error_code = "fuckme()"

    def test_normal_code(self):
        loader = CodeLoader('test_loader')
        mod = loader.create_module('test_module', self.normal_code)
        self.assertIsNotNone(mod)
        self.assertEqual(mod.test_function('fuck'), 'fuck')
        tc = mod.TestClass('fuck')
        self.assertEqual(tc.name, 'fuck')

    def test_dummy_backends(self):
        loader = CodeLoader('test_loader')
        mod = loader.create_module('test_module', self.normal_code)
        loader.save(mod, cahed=True)
        new_module = loader.load('test_module')
        self.assertIsNotNone(new_module)
        self.assertEqual(new_module.test_function('name'), 'name')

        loader.save(mod, cahed=False)
        new_module = loader.load('test_module')
        self.assertIsNotNone(new_module)
        self.assertEqual(new_module.test_function('name'), 'name')

    def test_syntax_error(self):
        loader = CodeLoader('test_loader')
        self.assertIsNone(loader.create_module('test_module', self.syntax_error_code))

    def test_runtime_error(self):
        loader = CodeLoader('test_loader')
        self.assertIsNone(loader.create_module('test_module', self.runtime_error_code))