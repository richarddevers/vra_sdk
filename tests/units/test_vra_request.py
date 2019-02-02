# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, MagicMock, call
from pytest import mark
from vra_sdk.vra_request import VraRequest
from vra_sdk.vra_exceptions import VraSdkConfigException, VraSdkRequestException, VraSdkMainRequestException
import json
from requests.exceptions import RequestException
from ..setup_test import SetupTest

@mark.test_unit
@patch('vra_sdk.vra_request.VraConfig')
class TestVraRequest(SetupTest):
    def test_init(self, mock_config):
        result = VraRequest('fake_payload')

        self.assertEqual(result.payload, 'fake_payload')
        self.assertEqual(result.response, None)

    def test_format_filters_raises_not_object_type(self, mock_config):
        mock_config.return_value.config = {'business_models': {'vm': ''}}

        with self.assertRaises(VraSdkConfigException):
            VraRequest('').format_filters('fake_object_type', '', '')

    @patch('vra_sdk.vra_request.get_module_class')
    def test_format_filters_raises_get_module_class(self, mock_module, mock_config):
        mock_module.side_effect = Exception()
        mock_config.return_value.config = {'business_models': {'vm': ''}}

        with self.assertRaises(VraSdkConfigException):
            VraRequest('').format_filters('vm', '', '')

    @patch('vra_sdk.vra_request.getattr')
    @patch('vra_sdk.vra_request.get_module_class')
    def test_format_filters(self, mock_module, mock_attr, mock_config):
        mock_module.return_value = 'fake_module', 'fake_class'
        mock_config.return_value.config_file = {
            'business_models': {'vm': {'path':'fake_module_class'}}}
        mock_attr.return_value = ['FAKE_RESOURCE_TYPE']

        result = VraRequest('').format_filters(
            'vm', 'fake_key', 'fake_value')

        mock_module.assert_called_once_with('fake_module_class')
        mock_attr.assert_called_once_with('fake_module', 'RESOURCE_TYPE')
        self.assertEqual(
            result, "$filter=(((resourceType/name+eq+'FAKE_RESOURCE_TYPE'))+and+(fake_key+eq+'fake_value'))")

    def test_get_status_raises(self, mock_config):
        with self.assertRaises(VraSdkRequestException):
            mock_config.return_value.session.get.side_effect = RequestException()
            VraRequest('').get_status()

    @patch('vra_sdk.vra_request.json.loads')
    def test_get_status_raises_unmanaged(self, mock_json, mock_config):
        mock_json.side_effect = Exception()

        with self.assertRaises(VraSdkMainRequestException):
            VraRequest('').get_status()

    def test_get_status(self, mock_config):
        mock_config.return_value.session.get.return_value.text = '{"state":"OK"}'

        result = VraRequest('').get_status()

        self.assertEqual(result, 'OK')

    def test_execute_async_(self, mock_config):
        mock_payload = MagicMock()
        mock_payload.execute_request.return_value.headers = {'NoLocation': ''}

        vra_req = VraRequest(mock_payload).execute_async()

        self.assertEqual('NoLocationFound', vra_req.status_url)
        mock_payload.execute_request.assert_called_once

    @patch('vra_sdk.vra_request.VraRequest.execute_async')
    @patch('vra_sdk.vra_request.VraRequest.get_status')
    def test_execute_sync_raises(self, mock_status, mock_exec, mock_config):
        mock_status.return_value = 'PROVIDER_FAILED'
        with self.assertRaises(VraSdkMainRequestException):
            VraRequest("").execute_sync()
        mock_exec.assert_called_once
        mock_status.assert_called_once

    @patch('vra_sdk.vra_request.VraRequest.execute_async')
    @patch('vra_sdk.vra_request.VraRequest.get_status')
    def test_execute_sync(self, mock_status, mock_exec, mock_config):
        mock_status.return_value = 'SUCCESSFUL'
        VraRequest("").execute_sync()
        mock_exec.assert_called_once
        mock_status.assert_called_once

    @patch('vra_sdk.vra_request.VraRequest.format_filters')
    def test_get_object_raw_not_vm(self, mock_format, mock_config):
        mock_config.return_value.verify = False
        mock_config.return_value.timeout = 12
        mock_config.return_value.vcac_server = 'fake_server'
        mock_format.return_value = "$filter=(((resourceType/name+eq+'FAKE_RESOURCE_TYPE'))+and+(fake_key+eq+'fake_value'))"
        mock_config.return_value.session.get.return_value.json.return_value = {
            "content": [{"id1": "fake_id1"}, {"id2": "fake_id2"}]}

        result = VraRequest('').get_object_raw(
            'notvm', 'key1', 'value1', 1, 1)

        self.assertEqual(result, [{'id1': 'fake_id1'}, {'id2': 'fake_id2'}])
        mock_config.return_value.session.get.assert_called_once_with(
            "https://fake_server/catalog-service/api/consumer/resources/?limit=1&page=1&$filter=(((resourceType/name+eq+'FAKE_RESOURCE_TYPE'))+and+(fake_key+eq+'fake_value'))", verify=False, timeout=12)

    @patch('vra_sdk.vra_request.VraRequest.format_filters')
    def test_get_object_vm_not_full_key_id(self, mock_format, mock_config):
        mock_config.return_value.config_file = {"virtual_machine_type":"vm"}
        mock_config.return_value.verify = False
        mock_config.return_value.timeout = 12
        mock_config.return_value.vcac_server = 'fake_server'
        mock_format.return_value = "$filter=(((resourceType/name+eq+'FAKE_RESOURCE_TYPE'))+and+(fake_key+eq+'fake_value'))"
        mock_config.return_value.session.get.return_value.json.side_effect = [{"content": [{"id": "fake_id1"}, {
            "id": "fake_id2"}]}, {'fake_res1': 'fake_value1'}, {'fake_res2': 'fake_value2'}]

        result = VraRequest('').get_object_raw(
            'vm', 'id', 'value1', 1, 1)

        mock_config.return_value.session.get.assert_any_call(
            "https://fake_server/catalog-service/api/consumer/resources/?limit=1&page=1&$filter=(((resourceType/name+eq+'FAKE_RESOURCE_TYPE'))+and+(fake_key+eq+'fake_value'))", verify=False, timeout=12)

        self.assertEqual(result, [{'id': 'fake_id1'}, {'id': 'fake_id2'}])

    @patch('vra_sdk.vra_request.VraRequest.format_filters')
    def test_get_object_vm_not_full_key_not_id(self, mock_format, mock_config):
        mock_config.return_value.config_file = {"virtual_machine_type":"vm"}
        mock_config.return_value.verify = False
        mock_config.return_value.timeout = 12
        mock_config.return_value.vcac_server = 'fake_server'
        mock_format.return_value = "$filter=(((resourceType/name+eq+'FAKE_RESOURCE_TYPE'))+and+(fake_key+eq+'fake_value'))"
        mock_config.return_value.session.get.return_value.json.side_effect = [{"content": [{"id": "fake_id1"}, {
            "id": "fake_id2"}]}, {'fake_res1': 'fake_value1'}, {'fake_res2': 'fake_value2'}]

        result = VraRequest('').get_object_raw(
            'vm', 'key1', 'value1', 1, 1)

        mock_config.return_value.session.get.assert_any_call(
            "https://fake_server/catalog-service/api/consumer/resources/?limit=1&page=1&$filter=(((resourceType/name+eq+'FAKE_RESOURCE_TYPE'))+and+(fake_key+eq+'fake_value'))", verify=False, timeout=12)

        self.assertEqual(result, [{'id': 'fake_id1'}, {'id': 'fake_id2'}])

    @patch('vra_sdk.vra_request.VraRequest.format_filters')
    def test_get_object_vm_full_key_id(self, mock_format, mock_config):
        mock_config.return_value.config_file = {"virtual_machine_type":"vm"}
        mock_config.return_value.verify = False
        mock_config.return_value.timeout = 12
        mock_config.return_value.vcac_server = 'fake_server'
        mock_format.return_value = "$filter=(((resourceType/name+eq+'FAKE_RESOURCE_TYPE'))+and+(fake_key+eq+'fake_value'))"
        mock_config.return_value.session.get.return_value.json.side_effect = [
                {"content": [{"id":"id1"}]},
                {"id":"id1", "fake_res1":"fake_value1"}
            ]

        result = VraRequest('').get_object_raw(
            'vm', 'id', 'id1', 1, 1,True)

        mock_config.return_value.session.get.assert_any_call(
            "https://fake_server/catalog-service/api/consumer/resources/?limit=1&page=1&$filter=(((resourceType/name+eq+'FAKE_RESOURCE_TYPE'))+and+(fake_key+eq+'fake_value'))", verify=False, timeout=12)
        mock_config.return_value.session.get.assert_any_call(
            'https://fake_server/catalog-service/api/consumer/resources/id1', verify=False, timeout=12)

        self.assertEqual(result, [{'id': 'id1', 'fake_res1': 'fake_value1'}])

    @patch('vra_sdk.vra_request.VraRequest.format_filters')
    def test_get_object_vm_full_key_not_id(self, mock_format, mock_config):
        mock_config.return_value.config_file = {"virtual_machine_type":"vm"}
        mock_config.return_value.verify = False
        mock_config.return_value.timeout = 12
        mock_config.return_value.vcac_server = 'fake_server'
        mock_format.return_value = "$filter=(((resourceType/name+eq+'FAKE_RESOURCE_TYPE'))+and+(fake_key+eq+'fake_value'))"
        mock_config.return_value.session.get.return_value.json.side_effect = [
                {"content": [{"id":"id1"},{"id":"id2"}]},
                {"id":"id1", "fake_res1":"fake_value1"},
                {"id":"id2","fake_res2": "fake_value2"}
            ]

        result = VraRequest('').get_object_raw(
            'vm', 'key1', 'value1', 1, 1,True)

        mock_config.return_value.session.get.assert_any_call(
            "https://fake_server/catalog-service/api/consumer/resources/?limit=1&page=1&$filter=(((resourceType/name+eq+'FAKE_RESOURCE_TYPE'))+and+(fake_key+eq+'fake_value'))", verify=False, timeout=12)
        mock_config.return_value.session.get.assert_any_call(
            'https://fake_server/catalog-service/api/consumer/resources/id1', verify=False, timeout=12)
        mock_config.return_value.session.get.assert_any_call(
            'https://fake_server/catalog-service/api/consumer/resources/id2', verify=False, timeout=12)

        self.assertEqual(result, [{'id': 'id1', 'fake_res1': 'fake_value1'}, {'id': 'id2', 'fake_res2': 'fake_value2'}])

    def test_get_request_result_raw_raises_request(self, mock_config):
        mock_config.return_value.session.get.side_effect = RequestException()
        with self.assertRaises(VraSdkRequestException):
            VraRequest('').get_request_result_raw()

    @patch('vra_sdk.vra_request.json')
    def test_get_request_result_raw_raises(self,mock_json, mock_config):
        mock_json.loads.side_effect=Exception()
        with self.assertRaises(VraSdkMainRequestException):
            VraRequest('').get_request_result_raw()

    @patch('vra_sdk.vra_request.json.loads')
    def test_get_request_result_raw_raises(self, mock_json, mock_config):
        mock_config.return_value.session.get.side_effect = RequestException()
        with self.assertRaises(VraSdkRequestException):
            VraRequest('').get_request_result_raw()

    def test_get_request_result_raw_content(self, mock_config):
        mock_config.return_value.verify = False
        mock_config.return_value.timeout = 12
        mock_config.return_value.vcac_server = 'fake_server'
        mock_config.return_value.session.get.return_value.text = '{"content": ["fake_data"]}'

        vra_request = VraRequest('')
        vra_request.status_url = "fake_status_url"
        result = vra_request.get_request_result_raw()

        self.assertEqual(result, 'fake_data')
        mock_config.return_value.session.get.assert_called_once_with(
            "fake_status_url/resources", verify=False, timeout=12)

    @patch('vra_sdk.vra_request.requests.session')
    def test_get_request_result_raw_no_content(self, mock_session, mock_config):
        mock_config.return_value.verify = False
        mock_config.return_value.timeout = 12
        mock_config.return_value.vcac_server = 'fake_server'
        mock_config.return_value.session.get.return_value.text = '{"fake_data":""}'

        vra_request = VraRequest('')
        vra_request.status_url = "fake_status_url"
        result = vra_request.get_request_result_raw()

        self.assertEqual(result, {'fake_data': ''})
        mock_config.return_value.session.get.assert_any_call(
            'fake_status_url/resources', verify=False, timeout=12)
        mock_config.return_value.session.get.assert_any_call(
            'fake_status_url/forms/details', verify=False, timeout=12)
