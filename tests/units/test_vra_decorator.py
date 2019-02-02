# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, MagicMock, call
from vra_sdk.vra_decorator import check_entitlement, update_catalog_resource_operation
from vra_sdk.vra_sdk import VraSdk
from vra_sdk.vra_exceptions import VraSdkEntitlementException, VraSdkException
import json
from pytest import mark


@mark.test_unit
class FakeClass():
    def __init__(self):
        self.catalog = {'fake_catalog': ''}
        self.config = MagicMock()

    @check_entitlement
    def fake_action(self, *args):
        pass

    @update_catalog_resource_operation
    def fake_action2(self, *args):
        pass


@mark.test_unit
class TestDecorator(unittest.TestCase):
    def test_check_entitlement_raises(self):
        with self.assertRaises(VraSdkEntitlementException):
            FakeClass().fake_action('fake_action')

    def test_check_entitlement(self):
        FakeClass().fake_action('fake_catalog')

    def test_update_catalog_resource_operation_raises(self):
        test_object = FakeClass()
        test_object.config.session.get.return_value.text = '{"operations":[{"name":"new_operation", "id":"new_id"}]}'
        with self.assertRaises(VraSdkException):
            test_object.fake_action2('operation')

    def test_update_catalog_resource_operation(self):
        test_object = FakeClass()
        test_object.config.verify=False
        test_object.config.timeout=12
        test_object.config.vcac_server = 'fake_server'
        test_object.config.session.get.return_value.text = '{"operations":[{"name":"new_operation", "id":"new_id"}]}'

        test_object.fake_action2('new_operation', 'fake_resource')

        self.assertEqual(test_object.catalog, {
                         'fake_catalog': '', 'new_operation': 'new_id'})
        test_object.config.session.get.assert_any_call('https://fake_server/catalog-service/api/consumer/resources/fake_resource', verify=False, timeout=12)
