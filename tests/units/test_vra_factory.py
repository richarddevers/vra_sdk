# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
from vra_sdk.vra_exceptions import VraSdkFactoryException, VraSdkConfigException
import sys
import os
from vra_sdk.vra_factory import VraFactory
from vra_sdk.models.vra_object import VraBaseObject
from ..setup_test import SetupTest
from pytest import mark


@mark.test_unit
@patch('vra_sdk.vra_factory.VraConfig')
class TestVraObject(SetupTest):
    def test_factory_raises_no_module_class(self, mock_config):
        mock_config.return_value.config = {'business_models': {}}

        with self.assertRaises(VraSdkConfigException):
            VraFactory.factory('missing_type')

    def test_factory_raises_no_module_class2(self, mock_config):
        mock_config.return_value.config = {
            'business_models': {'fake_type': ''}}

        with self.assertRaises(VraSdkConfigException):
            VraFactory.factory('missing_type')

    def test_factory_raises_not_authorized(self, mock_config):
        sys.path.append(os.path.abspath(os.path.join(
            os.path.dirname(__file__), "fixtures")))
        mock_config.return_value.config = {'business_models': {
            'fake_type': 'fake_business_model.FakeObject'}}

        with self.assertRaises(VraSdkConfigException):
            VraFactory.factory('fake_type', **{'fake_attr3': ''})

    def test_factory(self, mock_config):
        toto = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "fixtures"))
        sys.path.append(toto)
        mock_config.return_value.config_file = {'business_models': {
            'fake_type': {'path': 'fake_business_model.FakeObject'}}}

        my_object = VraFactory.factory(
            'fake_type', **{'fake_attr1': 'value1', 'fake_attr2': 'value2'})

        self.assertEqual(my_object.fake_attr1, 'value1')
        self.assertEqual(my_object.fake_attr2, 'value2')
        self.assertIsNone(my_object.fake_attr_empty)
