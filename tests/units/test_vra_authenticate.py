# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch
from ..setup_test import SetupTest
from vra_sdk.vra_authenticate import VraAuthenticate
from vra_sdk.vra_exceptions import VraSdkConfigException, VraSdkRequestException, VraSdkAuthenticateException
from requests.exceptions import RequestException
from pytest import mark


@mark.test_unit
class TestVraAuthenticate(SetupTest):

    @patch("vra_sdk.vra_authenticate.urllib3.disable_warnings")
    @patch("vra_sdk.vra_authenticate.VraConfig")
    def test_vra_authenticate_init(self, mock_config, mock_urllib3):
        env = "PRD"
        serv = "fake_server"

        mock_config.return_value.config = {
            'vcac_servers': {env: serv}, 'tenant': {env: ''}}
        authenticate = VraAuthenticate('PRD')

        mock_config.assert_called_once()
        mock_urllib3.assert_called_once()
        self.assertEqual(authenticate.environment, 'PRD')
        self.assertIsNone(authenticate.login)
        self.assertIsNone(authenticate.requestedFor)
        self.assertIsNone(authenticate.token)
        self.assertIsNone(authenticate.domain)

    @patch("vra_sdk.vra_authenticate.requests.Session")
    @patch("vra_sdk.vra_authenticate.urllib3.disable_warnings")
    @patch("vra_sdk.vra_authenticate.VraConfig")
    def test_auth_login_password_raises_no_domain(self, mock_config, mock_urllib3, mock_session):
        authenticate = VraAuthenticate('')
        mock_config.return_value.config = {'domain': ["fake_domain"]}

        with self.assertRaises(VraSdkConfigException):
            authenticate.auth_login_password("", "", "")

    @patch("vra_sdk.vra_authenticate.VraAuthenticate.get_token")
    @patch("vra_sdk.vra_authenticate.VraConfig")
    def test_auth_login_password(self, mock_config, mock_token):
        fake_login = "fake_login"
        fake_pwd = "fake_pwd"
        fake_domain = "fake_domain"
        fake_token = 'fake_token'

        mock_config.return_value.config_file = {'domain': [
            fake_domain], 'vcac_servers': {'PRD': 'fake_srv'}, 'tenant': {'PRD': ''}}
        mock_token.return_value = fake_token

        authenticate = VraAuthenticate('PRD')
        authenticate.auth_login_password(fake_login, fake_pwd, fake_domain)

        self.assertEqual(authenticate.login, fake_login)
        self.assertEqual(authenticate.domain, fake_domain)
        self.assertEqual(authenticate.token, fake_token)
        mock_token.assert_called_once()
        mock_token.assert_called_with(fake_login, fake_pwd)

    @patch("vra_sdk.vra_authenticate.requests.Session")
    @patch("vra_sdk.vra_authenticate.urllib3.disable_warnings")
    @patch("vra_sdk.vra_authenticate.VraConfig")
    def test_auth_login_token_raises_no_domain(self, mock_config, mock_urllib3, mock_session):
        authenticate = VraAuthenticate('')
        mock_config.return_value.config = {'domain': ["fake_domain"]}

        with self.assertRaises(VraSdkConfigException):
            authenticate.auth_login_token("", "", "")

    @patch("vra_sdk.vra_authenticate.VraConfig")
    def test_auth_login_token_(self, mock_config):
        fake_login = "fake_login"
        fake_domain = "fake_domain"
        fake_token = 'fake_token'

        mock_config.return_value.config_file = {'domain': [
            fake_domain], 'vcac_servers': {'PRD': 'fake_srv'}, 'tenant': {'PRD': ''}}

        authenticate = VraAuthenticate('PRD')
        authenticate.auth_login_token(fake_login, fake_token, fake_domain)

        self.assertEqual(authenticate.login, fake_login)
        self.assertEqual(authenticate.domain, fake_domain)
        self.assertEqual(authenticate.token, fake_token)

    @patch("vra_sdk.vra_authenticate.VraConfig")
    def test_get_token_raises_request(self, mock_config):
        mock_config.return_value.session.post.side_effect = RequestException()
        mock_config.return_value.config_file = {'domain': ['fake_domain'
                                                           ], 'vcac_servers': {'PRD': ''}, 'tenant': {'PRD': ''}}

        with self.assertRaises(VraSdkRequestException):
            VraAuthenticate('PRD').get_token("", "")

        mock_config.assert_called_once()

    @patch("vra_sdk.vra_authenticate.VraConfig")
    def test_get_token_raises(self, mock_config):
        # todo: add url check
        mock_config.return_value.session.post.side_effect = Exception()
        mock_config.return_value.config_file = {'domain': ['fake_domain'
                                                           ], 'vcac_servers': {'PRD': ''}, 'tenant': {'PRD': ''}}

        with self.assertRaises(VraSdkAuthenticateException):
            VraAuthenticate('PRD').get_token("", "")

        mock_config.return_value.session.post.assert_called_once()

    @patch("vra_sdk.vra_authenticate.VraConfig")
    def test_get_token(self, mock_config):
        mock_config.return_value.verify = False
        mock_config.return_value.timeout = 12
        fake_login = "fake_login"
        fake_pwd = "fake_pwd"
        fake_domain = "fake_domain"

        mock_config.return_value.session.post.return_value.status_code = 200
        mock_config.return_value.config_file = {'domain': [
            fake_domain], 'vcac_servers': {'PRD': 'fake_srv'}, 'tenant': {'PRD': ''}}
        mock_config.return_value.session.post.return_value.text = '{"id":"fake_token"}'
        authenticate = VraAuthenticate('PRD')

        authenticate.get_token(fake_login, fake_pwd)

        mock_config.return_value.session.post.assert_called_once_with('https://fake_srv/identity/api/tokens', data='{"username": "fake_login", "password": "fake_pwd", "tenant": ""}', headers={
            'Content-Type': 'application/json', 'Accept': 'application/json'}, timeout=12, verify=False)
