# -*- coding: utf-8; -*-

from unittest import TestCase


try:
    import sqlalchemy as sa
    from wuttjamaican.db import util as mod
    from wuttjamaican.db.model.base import Setting
except ImportError:
    pass
else:


    class TestModelBase(TestCase):

        def test_dict_behavior(self):
            setting = Setting()
            self.assertEqual(list(iter(setting)), [('name', None), ('value', None)])
            self.assertIsNone(setting['name'])
            setting.name = 'foo'
            self.assertEqual(setting['name'], 'foo')


    class TestUUIDColumn(TestCase):

        def test_basic(self):
            column = mod.uuid_column()
            self.assertIsInstance(column, sa.Column)
            self.assertIsInstance(column.type, sa.String)
            self.assertEqual(column.type.length, 32)


    class TestUUIDFKColumn(TestCase):

        def test_basic(self):
            column = mod.uuid_fk_column('foo.bar')
            self.assertIsInstance(column, sa.Column)
            self.assertIsInstance(column.type, sa.String)
            self.assertEqual(column.type.length, 32)
