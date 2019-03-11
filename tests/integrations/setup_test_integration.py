# -*- coding: utf-8 -*-
import os
import inspect
from unittest.mock import MagicMock


def get_test_config_file_path():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures', 'fake_config.json')


def get_side_effect_by_args(*args, **kwargs):
    m = MagicMock()
    if "/catalog-service/api/consumer/entitledCatalogItems?limit=998" in args[0]:
        # get_bg_id
        m.text = '{"content":[{"entitledOrganizations":[{"subtenantLabel":"fake_bg", "subtenantRef":"fake_bg_id"}]}]}'
    elif "/catalog-service/api/consumer/entitledCatalogItems?limit=9999" in args[0]:
        # get_catalog
        m.text = '{"content":[{"catalogItem":{"name":"fake_catalog_item", "id":"fake_catalog_item_id"}}]}'
    elif '/catalog-service/api/consumer/resources' in args[0]:
        # update_catalog_resource_operation
        m.text = '{"operations":[{"name":"fake_action_name", "id":"fake_action_id"}]}'
    elif 'FakeLocation' in args[0]:
        # get_status
        m.text = '{"state":"SUCCESSFUL"}'
    return m


def get_side_effect(*args, **kwargs):
    m = MagicMock()
    stack = [elt.function for elt in inspect.stack()]
    if 'get_bg_id' in stack:
        m.text = '{"content":[{"entitledOrganizations":[{"subtenantLabel":"fake_bg", "subtenantRef":"fake_bg_id"}]}]}'
    elif 'get_catalog' in stack:
        m.text = '{"content":[{"catalogItem":{"name":"fake_catalog_item", "id":"fake_catalog_item_id"}}]}'
    elif 'get_status' in stack:
        m.text = '{"state":"SUCCESSFUL"}'
    elif ('get_template' in stack) and ('request_catalog_item' in stack):
        m.text= '{"type": "com.vmware.vcac.catalog.domain.request.CatalogItemProvisioningRequest","catalogItemId": "xxxx","requestedFor": "xxxx","businessGroupId": "xxxxx","description":"","reasons":"","data":{"fake_data1":"","fake_data2":""}}'
    elif ('get_template' in stack) and ('request_resource_action' in stack):
        m.text= '{"type": "com.vmware.vcac.catalog.domain.request.CatalogResourceRequest","resourceId": "xxxx","actionId": "xxxxx","description":"","data": {"provider-__ASD_PRESENTATION_INSTANCE":"","fake_data_1":"","fake_data_2":""}}'
    elif 'wrapper' in stack:
        m.text = '{"operations":[{"name":"fake_action_name", "id":"fake_action_id"}]}'

    return m


def post_side_effect(*args, **kargs):
    m = MagicMock()
    if '/identity/api/tokens' in args[0]:
        # get_token
        m.text = '{"id":"fake_token"}'
    elif '/catalog-service/api/consumer/entitledCatalogItems/fake_catalog_item_id/requests':
        # payload7 catalog_item execute_request
        m.headers = {'Location': 'fake_status_url'}
    return m
