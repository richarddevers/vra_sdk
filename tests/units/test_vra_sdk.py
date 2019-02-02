# -*- coding: utf-8 -*-


import unittest
from ..setup_test import SetupTest
from unittest.mock import patch, MagicMock, call, mock_open
from vra_sdk.vra_sdk import VraSdk
from vra_sdk.vra_request import VraRequest
from vra_sdk.vra_exceptions import VraSdkMainException, VraSdkRequestException
from pytest import mark
from requests.exceptions import RequestException


@mark.test_unit
@patch('vra_sdk.vra_sdk.VraSdk.get_catalog')
@patch('vra_sdk.vra_sdk.VraConfig')
class TestVraSdkBgId(SetupTest):

    def test_get_bg_id_raises_no_content(self, mock_config, mock_catalog):
        mock_config.return_value.session.get.return_value.text = '{"no_content":""}'

        with self.assertRaises(VraSdkMainException):
            VraSdk(MagicMock(), "")

        mock_config.return_value.session.get.assert_called_once()
        mock_config.return_value.session.get.return_value.raise_for_status.assert_called_once()

    def test_get_bg_id_raises_no_business_group(self, mock_config, mock_catalog):
        mock_config.return_value.session.get.return_value.text = '{"content":[{"entitledOrganizations":[{"subtenantLabel":"wrong_bg"}]}]}'

        with self.assertRaises(VraSdkMainException):
            VraSdk(MagicMock(), "")

        mock_config.return_value.session.get.assert_called_once()
        mock_config.return_value.session.get.return_value.raise_for_status.assert_called_once()

    def test_request_bg_id(self, mock_config, mock_catalog):
        mock_config.return_value.verify = False
        mock_config.return_value.timeout = 12
        authentication_object = MagicMock()
        mock_config.return_value.vcac_server = 'fake_server'
        mock_config.return_value.session.get.return_value.text = '{"content":[{"entitledOrganizations":[{"subtenantLabel":"bg_label", "subtenantRef":"fake_bg_id"}]}]}'

        vra_sdk = VraSdk(authentication_object, "bg_label")

        self.assertEqual(vra_sdk.business_group_id, "fake_bg_id")
        mock_config.return_value.session.get.assert_called_once_with(
            'https://fake_server/catalog-service/api/consumer/entitledCatalogItems?limit=998', verify=False, timeout=12)
        mock_config.return_value.session.get.return_value.raise_for_status.assert_called_once()


@mark.test_unit
@patch('vra_sdk.vra_sdk.VraSdk.get_bg_id')
@patch('vra_sdk.vra_sdk.VraConfig')
class TestVraSdkGetCatalog(SetupTest):
    def test_get_catalog_raises_get(self, mock_config, mock_get_bg_id):
        mock_config.return_value.session.get.side_effect = RequestException()

        with self.assertRaises(VraSdkRequestException):
            VraSdk(MagicMock(), "").get_catalog()

        mock_config.return_value.session.get.assert_called_once()

    @patch('vra_sdk.vra_sdk.os')
    @patch('vra_sdk.vra_sdk.json')
    @patch('vra_sdk.vra_sdk.vra_utils.resolve_path')
    def test_get_catalog_raises_json(self, mock_resolve, mock_json, mock_os, mock_config, mock_get_bg_id):
        authentication_object = MagicMock()
        mock_json.loads.side_effect = Exception()

        with self.assertRaises(VraSdkMainException):
            VraSdk(authentication_object, "").get_catalog()
        mock_json.loads.assert_called_once()

    @patch('vra_sdk.vra_sdk.os')
    @patch('vra_sdk.vra_sdk.vra_utils.resolve_path')
    def test_get_catalog(self, mock_resolve, mock_os, mock_config, mock_get_bg_id):
        mock_config.return_value.verify = False
        mock_config.return_value.timeout = 12
        mock_config.return_value.vcac_server = 'fake_server'
        mock_config.return_value.session.get.return_value.text = '{"content":[{"catalogItem":{"name":"fake_name","id":"fake_id"}}]}'

        VraSdk(MagicMock(), "").get_catalog()

        mock_config.return_value.session.get.assert_any_call(
            'https://fake_server/catalog-service/api/consumer/entitledCatalogItems?limit=9999', verify=False, timeout=12)


@mark.test_unit
@patch('vra_sdk.vra_sdk.VraSdk.get_bg_id')
@patch('vra_sdk.vra_sdk.VraSdk.get_catalog')
@patch('vra_sdk.vra_sdk.VraConfig')
class TestVraSdk(SetupTest):
    def test_init(self, mock_config, mock_get_catalog, mock_get_bg_id):
        mock_get_bg_id.return_value = 'fake_bg_id'
        authentication_object = MagicMock()
        authentication_object.domain = "fake_domain"
        mock_get_catalog.return_value = "fake_catalog"

        vra_sdk = VraSdk(authentication_object, "fake_bg")

        self.assertEqual(vra_sdk.catalog, "fake_catalog")
        self.assertEqual(vra_sdk.business_group, "fake_bg")
        self.assertEqual(vra_sdk.business_group_id, "fake_bg_id")
        mock_get_catalog.assert_called_once()
        mock_get_bg_id.assert_called_once()

    @patch('vra_sdk.vra_sdk.VraRequest')
    @patch('vra_sdk.vra_sdk.VraSdk.format_payload')
    def test_request_catalog_item(self, mock_payload, mock_request, mock_config, mock_get_catalog, mock_get_bg_id):
        mock_payload.return_value = 'fake_payload'
        mock_config.return_value.config_file = {'payload_default_version': 7}
        vra_sdk = VraSdk(MagicMock(), "")

        undecorrated = vra_sdk.request_catalog_item.__wrapped__
        fake_kwargs = {"fake_kwargs": ""}

        result = undecorrated(vra_sdk, 'fake_catalog_name', **fake_kwargs)

        fake_kwargs['payload_version'] = 7
        mock_payload.assert_called_once_with(
            'catalog_item', 'fake_catalog_name', None, **fake_kwargs)
        mock_request.assert_called_once_with(
            'fake_payload')

    @patch('vra_sdk.vra_sdk.VraRequest')
    @patch('vra_sdk.vra_sdk.VraSdk.format_payload')
    def test_request_resource_action(self, mock_payload, mock_request, mock_config, mock_get_catalog, mock_get_bg_id):
        mock_config.return_value.config_file = {'payload_default_version': 7}
        mock_payload.return_value = 'fake_payload'
        vra_sdk = VraSdk(MagicMock(), "")

        fake_kwargs = {"fake_key": "fake_value"}
        undecorrated = vra_sdk.request_resource_action.__wrapped__.__wrapped__
        undecorrated(vra_sdk, 'fake_action_name',
                              'fake_resource_id', **fake_kwargs)

        fake_kwargs['payload_version'] = 7
        mock_payload.assert_called_once_with(
            'resource_action', 'fake_action_name', 'fake_resource_id', None, **fake_kwargs)
        mock_request.assert_called_once_with('fake_payload')

    @patch('vra_sdk.vra_sdk.VraRequest')
    def test_get_data(self, mock_request, mock_config, mock_catalog, mock_get_bg_id):
        mock_request.return_value.get_object.return_value = ['fake_data']
        vra_sdk = VraSdk(MagicMock(), '')

        vra_sdk.get_data('vm', 'key', 'value')

        mock_request.return_value.get_object.assert_called_once_with(
            'vm', 'key', 'value', 1 , 1, True)

    @patch('vra_sdk.vra_sdk.VraRequest')
    def test_get_data_raises(self, mock_request, mock_config, mock_catalog, mock_get_bg_id):
        mock_request.return_value.get_object.return_value = None
        vra_sdk = VraSdk(MagicMock(), '')
        with self.assertRaises(VraSdkMainException):
            vra_sdk.get_data('', '', '')
