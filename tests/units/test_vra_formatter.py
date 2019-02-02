# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, call
import vra_sdk.vra_formatter
from ..setup_test import SetupTest
from pytest import mark


@mark.test_unit
class TestVraFormatter(SetupTest):

    def test_parse_string(self):
        data_to_test = {"key": "result_key",
                        "value": {"value": "result_value"}}
        expected_result = "result_key", "result_value"
        result = vra_sdk.vra_formatter.parse_string(data_to_test)
        self.assertEqual(expected_result, result)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], str)

    def test_parse_string_without_key(self):
        data_to_test = {"value": "result_value"}
        expected_result = "result_value"
        result = vra_sdk.vra_formatter.parse_string_without_key(data_to_test)
        self.assertEqual(expected_result, result)
        self.assertIsInstance(result, str)

    def test_parse_integer(self):
        data_to_test = {"key": "result_key", "value": {"value": 10}}
        expected_result = "result_key", 10
        result = vra_sdk.vra_formatter.parse_integer(data_to_test)
        self.assertEqual(expected_result, result)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], int)

    def test_parse_decimal(self):
        data_to_test = {"key": "result_key", "value": {"value": 10.01}}
        expected_result = "result_key", 10.01
        result = vra_sdk.vra_formatter.parse_decimal(data_to_test)
        self.assertEqual(expected_result, result)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], float)

    def test_parse_boolean(self):
        data_to_test = {"key": "result_key", "value": {"value": True}}
        expected_result = "result_key", True
        result = vra_sdk.vra_formatter.parse_boolean(data_to_test)
        self.assertEqual(expected_result, result)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], bool)

    def test_parse_datetime(self):
        data_to_test = {"key": "result_key", "value": {
            "value": "2018-12-20T22:37:45.000+0100"}}
        expected_result = "result_key", "2018-12-20T22:37:45.000+0100"
        result = vra_sdk.vra_formatter.parse_datetime(data_to_test)
        self.assertEqual(expected_result, result)

    @patch('vra_sdk.vra_formatter.parse_key')
    def test_parse_multiple(self, mock_parse_key):
        item_to_test = ""
        data_to_test = {"key": "key0", "value": {"items": [item_to_test]}}
        mock_parse_key.return_value = "key0", "string1"
        expected_result = "key0", ["string1"]

        result = vra_sdk.vra_formatter.parse_multiple(data_to_test)

        self.assertEqual(expected_result, result)
        mock_parse_key.assert_called_once_with(item_to_test)

    @patch('vra_sdk.vra_formatter.parse_string_without_key')
    @patch('vra_sdk.vra_formatter.parse_key')
    def test_parse_multiple_raises(self, mock_parse_key, mock_parse_without_key):
        item_to_test = ""
        data_to_test = {"key": "key0", "value": {"items": [item_to_test]}}
        mock_parse_key.side_effect = TypeError
        mock_parse_without_key.return_value = "string1"
        expected_result = "key0", ["string1"]

        result = vra_sdk.vra_formatter.parse_multiple(data_to_test)

        self.assertEqual(expected_result, result)
        mock_parse_key.assert_called_once_with(item_to_test)
        mock_parse_without_key.assert_called_once_with(item_to_test)

    @patch('vra_sdk.vra_formatter.parse_key')
    def test_parse_multiple_2_iter(self, mock_parse_key):
        item_to_test1 = ""
        item_to_test2 = ""
        data_to_test = {"key": "key0", "value": {
            "items": [item_to_test1, item_to_test2]}}
        mock_parse_key.return_value = "key0", "string1"
        expected_result = "key0", ["string1", "string1"]
        calls = [call(item_to_test1), call(item_to_test2)]

        result = vra_sdk.vra_formatter.parse_multiple(data_to_test)

        mock_parse_key.assert_has_calls(calls)
        self.assertEqual(expected_result, result)
        self.assertEqual(mock_parse_key.call_count, 2)

    @patch('vra_sdk.vra_formatter.parse_string_without_key')
    @patch('vra_sdk.vra_formatter.parse_key')
    def test_parse_multiple_raises_2_iter(self, mock_parse_key, mock_parse_without_key):
        item_to_test1 = ""
        item_to_test2 = ""
        data_to_test = {"key": "key0", "value": {
            "items": [item_to_test1, item_to_test2]}}
        mock_parse_key.side_effect = TypeError
        mock_parse_without_key.return_value = "string1"
        expected_result = "key0", ["string1", "string1"]
        calls = [call(item_to_test1), call(item_to_test2)]

        result = vra_sdk.vra_formatter.parse_multiple(data_to_test)

        self.assertEqual(expected_result, result)
        mock_parse_key.assert_has_calls(calls)
        mock_parse_without_key.assert_has_calls(calls)
        self.assertEqual(mock_parse_key.call_count, 2)

    @patch('vra_sdk.vra_formatter.parse_key')
    def test_parse_complex_with_values_and_key(self, mock_parse_key):
        entry_to_test = ""
        data_to_test = {"key": "key0", "values": {"entries": [entry_to_test]}}
        mock_parse_key.return_value = "key1", "value"
        expected_result = "key0", {"key1": "value"}

        result = vra_sdk.vra_formatter.parse_complex(data_to_test)

        self.assertEqual(expected_result, result)
        mock_parse_key.assert_called_once_with(entry_to_test)

    @patch('vra_sdk.vra_formatter.parse_key')
    def test_parse_complex_with_values_and_no_key(self, mock_parse_key):
        entry_to_test = ""
        data_to_test = {"values": {"entries": [entry_to_test]}}
        mock_parse_key.return_value = "key1", "value"
        expected_result = "0", {"key1": "value"}

        result = vra_sdk.vra_formatter.parse_complex(data_to_test)

        self.assertEqual(expected_result, result)
        mock_parse_key.assert_called_once_with(entry_to_test)

    @patch('vra_sdk.vra_formatter.parse_key')
    def test_parse_complex_no_values_with_key(self, mock_parse_key):
        entry_to_test = ""
        data_to_test = {"key": "key0", "value": {
            "values": {"entries": [entry_to_test]}}}
        mock_parse_key.return_value = "key1", "value"
        expected_result = "key0", {"key1": "value"}

        result = vra_sdk.vra_formatter.parse_complex(data_to_test)

        self.assertEqual(expected_result, result)
        mock_parse_key.assert_called_once_with(entry_to_test)

    @patch('vra_sdk.vra_formatter.parse_key')
    def test_parse_complex_no_values_no_key(self, mock_parse_key):
        entry_to_test = ""
        data_to_test = {"value": {"values": {"entries": [entry_to_test]}}}
        mock_parse_key.return_value = "key1", "value"
        expected_result = "0", {"key1": "value"}

        result = vra_sdk.vra_formatter.parse_complex(data_to_test)

        self.assertEqual(expected_result, result)
        mock_parse_key.assert_called_once_with(entry_to_test)

    @patch('vra_sdk.vra_formatter.parse_key')
    def test_parse_complex_no_values_no_key_2_iter(self, mock_parse_key):
        entry1 = ""
        entry2 = ""
        entry_to_test = [entry1, entry2]
        data_to_test = {"value": {"values": {"entries": entry_to_test}}}
        mock_parse_key.return_value = [("key1", "value1"), ("key2", "value2")]
        expected_result = "0", {("key1", "value1"): ("key2", "value2")}
        calls = [call(entry1), call(entry2)]

        result = vra_sdk.vra_formatter.parse_complex(data_to_test)

        self.assertEqual(expected_result, result)
        mock_parse_key.assert_has_calls(calls)
        self.assertEqual(mock_parse_key.call_count, 2)

    @patch('vra_sdk.vra_formatter.parse_string')
    def test_parse_key_with_value(self, mock_parse_string):
        data_to_test = {"value": {"type": "string"}}
        vra_sdk.vra_formatter.parse_key(data_to_test)
        mock_parse_string.assert_called_once()
        mock_parse_string.asser_called_with(data_to_test)

    @patch('vra_sdk.vra_formatter.parse_string')
    def test_parse_key_without_value(self, mock_parse_string):
        data_to_test = {"type": "string"}
        vra_sdk.vra_formatter.parse_key(data_to_test)
        mock_parse_string.assert_called_once()
        mock_parse_string.asser_called_with(data_to_test)

    @patch('vra_sdk.vra_formatter.parse_key')
    def test_format_result_with_values(self, mock_parse_key):
        # This test does not mock vra_utils.prettify_keys since it would mock the whole thing :/
        entries = {"key": "provider-fake_param",
                   "value": {"type": "string", "value": "fake_value"}}

        data_to_test = {"values": {"entries": [entries]}, "id": "fake_id", "name": "fake_name", "status": "fake_status",
                        "description": "fake_description", "organization": {"subtenantRef": "fake_subRef", "subtenantLabel": "fake_subLabel"}}

        expected_result = {"fake_param": "fake_value", "id": "fake_id", "name": "fake_name", "status": "fake_status",
                           "description": "fake_description", "business_group": {"id": "fake_subRef", "label": "fake_subLabel"}}

        mock_parse_key.return_value = "provider-fake_param", "fake_value"

        result = vra_sdk.vra_formatter.format_result(data_to_test)

        self.assertEqual(expected_result, result)
        mock_parse_key.assert_called_once_with(entries)

    @patch('vra_sdk.vra_formatter.parse_key')
    def test_format_result_with_resource_data(self, mock_parse_key):
        # This test does not mock vra_utils.prettify_keys since it would mock the whole thing :/
        entries = {"key": "provider-fake_param",
                   "value": {"type": "string", "value": "fake_value"}}

        data_to_test = {"resourceData": {"entries": [entries]}, "id": "fake_id", "name": "fake_name", "status": "fake_status",
                        "description": "fake_description", "organization": {"subtenantRef": "fake_subRef", "subtenantLabel": "fake_subLabel"}}

        expected_result = {"fake_param": "fake_value", "id": "fake_id", "name": "fake_name", "status": "fake_status",
                           "description": "fake_description", "business_group": {"id": "fake_subRef", "label": "fake_subLabel"}}

        mock_parse_key.return_value = "provider-fake_param", "fake_value"

        result = vra_sdk.vra_formatter.format_result(data_to_test)

        self.assertEqual(expected_result, result)
        mock_parse_key.assert_called_once_with(entries)

    @patch('vra_sdk.vra_formatter.parse_key')
    def test_format_result_with_values_2_iter(self, mock_parse_key):
        # This test does not mock vra_utils.prettify_keys since it would mock the whole thing :/
        entries = [{"key": "provider-fake_param", "value": {"type": "string", "value": "fake_value"}},
                   {"key": "provider-fake_param2", "value": {"type": "string", "value": "fake_value2"}}]

        data_to_test = {"values": {"entries": entries}, "id": "fake_id", "name": "fake_name", "status": "fake_status",
                        "description": "fake_description", "organization": {"subtenantRef": "fake_subRef", "subtenantLabel": "fake_subLabel"}}

        expected_result = {'id': 'fake_id', 'name': 'fake_name', 'status': 'fake_status', 'description': 'fake_description', 'business_group': {
            'id': 'fake_subRef', 'label': 'fake_subLabel'}, 'fake_param': 'fake_value', 'fake_param2': 'fake_value'}
        mock_parse_key.return_value = "provider-fake_param", "fake_value"
        calls = [call(entries[0]), call(entries[1])]
        result = vra_sdk.vra_formatter.format_result(data_to_test)

        self.assertEqual(expected_result, result)
        mock_parse_key.assert_has_calls(calls)
        self.assertEqual(2, mock_parse_key.call_count)
