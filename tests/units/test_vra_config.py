# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, mock_open
import json
from vra_sdk.vra_config import VraConfig
from ..setup_test import SetupTest
from pytest import mark


@mark.test_unit
class TestVraConfig(SetupTest):
    @patch('vra_sdk.vra_config.open', new_callable=mock_open, read_data='{"fake_config":""}')
    def test_init(self, mock_oppen):
        result = VraConfig('fake.json')
        self.assertEqual(result.config_file, {'fake_config': ''})
