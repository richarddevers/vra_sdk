# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
import vra_sdk.vra_utils
from pytest import mark
from ..setup_test import SetupTest


@mark.test_unit
class TestVraUtils(SetupTest):
    def test_to_snake_case_ok(self):
        test_str = "AzerTy"
        result = vra_sdk.vra_utils.to_snake_case(test_str)
        expected_result = "azer_ty"
        self.assertEqual(result, expected_result)

    @patch('vra_sdk.vra_utils.to_snake_case')
    def test_prettify_key(self, mock_to_snake):
        data = {"FakeKey": "fake_result"}
        mock_to_snake.return_value = "fake_key"
        result = vra_sdk.vra_utils.prettify_key(data)
        expected_result = {"fake_key": "fake_result"}
        mock_to_snake.assert_called_once_with("FakeKey")
        self.assertEqual(result, expected_result)

    def test_clean_kwargs(self):
        kwargs = {'fake.key':'fake_value'}
        result = vra_sdk.vra_utils.clean_kwargs_key(**kwargs)
        self.assertIn('fake_key', result)
        self.assertEqual(result.get('fake_key'), 'fake_value')