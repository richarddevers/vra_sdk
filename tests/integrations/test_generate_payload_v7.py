# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, MagicMock
from vra_sdk.vra_authenticate import VraAuthenticate
from vra_sdk.vra_sdk import VraSdk
import inspect
from vra_sdk.vra_config import VraConfig
import os
from ..setup_test import SetupTest
from .setup_test_integration import *
from .cerberus_custom_7 import CerberusCustomValidator7
from pytest import mark


@mark.test_integration
@patch('requests.Session')
class TestIntegration7(SetupTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validator = CerberusCustomValidator7()

    def test_validate_payload_7(self, mock_session):
        mock_session.return_value.get.side_effect = get_side_effect
        mock_session.return_value.post.side_effect = post_side_effect

        VraConfig(get_test_config_file_path())
        auth = VraAuthenticate('PRD').auth_login_password(
            'fake_login', 'fake_password', 'foo.fuu.com')
        sdk = VraSdk(auth, 'fake_bg')

        data = {"fake_data1": "fake_value1", "fake_data2": 122}

        fake_item_request = sdk.request_catalog_item(
            "fake_catalog_item", **data)
        self.assertTrue(self.validator.catalog_item(
            fake_item_request.payload.customized))

        fake_action_request = sdk.request_resource_action(
            "fake_action_name", "fake_resource_id", **data)
        self.assertTrue(self.validator.resource_action(
            fake_action_request.payload.customized))