# -*- coding:utf-8 -*-

import json
import unittest
import datetime
from sqlalchemy import (Column, Text, Integer, DateTime)
from sqlalchemy.dialects.postgresql import (ARRAY, JSON)
from sqlalchemy.ext.declarative import declarative_base
from .validate import datetime2utmp, safe_int_arg
from ._sqlalchemy import DBFC

__author__ = 'winkidney'


class TestObj(declarative_base()):
    __tablename__ = 'test fucker'

    name = Column(Text)
    integer = Column(Integer, primary_key=True)
    slist = Column(ARRAY(Text))
    ilist = Column(ARRAY(Integer))
    date = Column(DateTime)
    json = Column(JSON)


class TestDBFC(unittest.TestCase):

    def test_instance(self):
        now = datetime.datetime.now()
        test_obj = TestObj(
            name='hehe',
            integer=1,
            slist=['fuck', 'you', 'ass'],
            ilist=[1,2,3],
            date=now,
            json={'key':'value'}
        )

        expected_result = {
            'name': 'hehe',
            'integer': 1,
            'slist': 'fuck,you,ass',
            'ilist': '1,2,3',
            'date': datetime2utmp(now),
            'json': json.dumps({'key':'value'}),
        }
        dbfc = DBFC(test_obj, allow_output=['name', ])
        self.assertEqual(dbfc.as_dict(pure=True), expected_result)
        self.assertEqual(dbfc.as_dict(), {'name': 'hehe'})
        self.assertEqual(list(dbfc.as_list()), [('name', 'hehe')])

    def test_specified_registry(self):
        from _sqlalchemy import DBFC
        test_obj = TestObj(
            name='hehe',
        )

        expected_result = {
            'name': 'hehe',
        }
        dbfc = DBFC(test_obj, allow_output=('name',), registry={Text: lambda x: x[-1]})
        self.assertEqual(dbfc.as_dict(), {'name': 'e'})

    def test_unkonw_field(self):
        from _sqlalchemy import DBFC
        DBFC.unregister(ARRAY)
        test_obj = TestObj(
            slist=['fuck', 'you', 'ass'],
        )

        expected_result = {
            'slist': ['fuck', 'you', 'ass'],
        }
        dbfc = DBFC(test_obj, allow_output=('slist',))
        self.assertEqual(dbfc.as_dict(), expected_result)


class TestValidate(unittest.TestCase):

    def testsafe_int_arg(self):
        default = 10
        self.assertEqual(safe_int_arg('5', default), 5)
        self.assertEqual(safe_int_arg(None, default), 10)
        self.assertEqual(safe_int_arg("fuck", default), 10)

        self.assertEqual(safe_int_arg('5', default, nmin=1, nmax=12), 5)
        self.assertEqual(safe_int_arg('13', default, nmin=1, nmax=12), 10)
        self.assertEqual(safe_int_arg('-1', default, nmin=1, nmax=12), 10)
        self.assertEqual(safe_int_arg('1', default, nmin=1, nmax=12), 1)
        self.assertEqual(safe_int_arg('-1', default, nmin=1), 10)
        self.assertEqual(safe_int_arg('20', default, nmax=12), 10)


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


