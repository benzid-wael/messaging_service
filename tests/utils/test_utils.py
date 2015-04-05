# -*- coding: utf-8 -*-

import pytest

from service.handlers.utils import load_class
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
        
