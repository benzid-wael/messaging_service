# -*- coding: utf-8 -*-

import pytest

from service.exceptions import ImproperlyConfigured
from service.utils import load_class, load_handlers
from service.handlers.base import BaseHandler


class TestLoader:

    def test_loader_success(self):
        base_handler = load_class("service.handlers.base.BaseHandler")
        assert issubclass(base_handler, BaseHandler) == True
        assert base_handler.__name__ == 'BaseHandler'

    def test_module_does_not_exist(self):
        with pytest.raises(AttributeError):
            load_class("service.handlers.no_such_module")

    def test_class_does_not_exist(self):
        with pytest.raises(AttributeError):
            load_class("service.handlers.base.NoClass")

    def test_nomodule_noclass(self):
        with pytest.raises(ImportError):
            load_class("service.handlers.no_such_module.NoModule")

    def test_no_dotted_path(self):
        with pytest.raises(AttributeError):
            load_class("NoModule")


class FakeSettings(object):
    def __init__(self, settings):
        self.MESSAGE_QUEUE = settings


class TestLoadHandlers:

    settings_cases = (
        ({}, KeyError),
        ({'handlers': {}}, {}),
        ({'handlers': {'sms': {'class': 'service.handlers.NoHandler'}}},
         AttributeError),
        ({'handlers': {'sms': {'class': 'service.no_module.NoHandler'}}},
         ImportError),
        (
            {'handlers': {
                'sms': {'class': 'tests.utils.fake_handler.MyHandler'}}},
            {'sms': BaseHandler}),
    )

    def test_simple_cases(self):
        for case, expected in self.settings_cases:
            try:
                my_setting = FakeSettings(case)
                result = load_handlers(my_setting)
                for k, expected_class in expected.items():
                    assert isinstance(result[k], expected_class)
            except AssertionError:
                raise
            except Exception as e:
                assert isinstance(e, expected)

    def test_bad_handler(self):
        handler_setting = {
            'handlers': {
                'sms': {'class': 'tests.utils.fake_handler.BadHandler'}
            }
        }
        my_setting = FakeSettings(handler_setting)
        with pytest.raises(ImproperlyConfigured):
            load_handlers(my_setting)
