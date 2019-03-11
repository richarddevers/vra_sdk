# -*- coding: utf-8 -*-
from vra_sdk.models.vra_object import VraBaseObject
from vra_sdk.vra_config import VraConfig
from vra_sdk.vra_utils import load_payload_file
from vra_sdk.vra_exceptions import VraSdkRequestException, VraSdkPayloadException
import requests
import json
from copy import deepcopy 

class BasePayload():
    """Base class for CatalogItem and ResourceAction
    """

    def __init__(self):
        self.config = VraConfig()

    def customize_payload(self, payload, **kwargs):
        """base customization payload
        
        Args:
            payload (dict): base payload, without any customization
        
        Returns:
            dict: customized payload
        """

        if kwargs['payload_type'] == 'CatalogItem':
            payload['catalogItemId'] = kwargs['catalog_item_id']
            payload['requestedFor'] = kwargs['requested_for']
            payload['businessGroupId'] = kwargs['business_group_id']
        else:
            payload['actionId'] = kwargs['resource_action_id']
            payload['resourceId'] = kwargs['resource_id']
            if 'description' in kwargs:
                payload['description'] = kwargs['description']

        key_to_performed = [key for key in kwargs.keys() if key not in self.config.config_file['not_in_data']]
        for key in key_to_performed:
            payload['data'][key] = kwargs[key]

        return payload


class CatalogItem(BasePayload):

    def __init__(self, customization_func=None, **kwargs):
        """Init ResourceAction object for vRa 7.x payload object
            customization_func ([type], optional): Defaults to None. If not None, this function will add a second customization after the initial one.
        """

        super().__init__()
        self.customized = None
        if not kwargs.get('payload_path'):
            self.base = self.get_template(kwargs.get('catalog_item_id'))
        else:
            self.base = load_payload_file(kwargs['payload_path'])

        self.customized = self.customize_payload(deepcopy(self.base), **kwargs)
        if customization_func:
            self.customized = customization_func(self.customized, **kwargs)

    def execute_request(self):
        """Execute the request against the vRa infrastructure
        
        Returns:
            requests.Request: request object
        """

        try:
            req = self.config.session.post(
                f"https://{self.config.vcac_server}/catalog-service/api/consumer/entitledCatalogItems/{self.customized['catalogItemId']}/requests",
                json=self.customized,
                verify=self.config.verify,
                timeout=self.config.timeout)
            req.raise_for_status()
            return req
        except requests.exceptions.RequestException as e:
            raise VraSdkRequestException(
                f'vRa request exception : {e}')
        except Exception as e:
            raise VraSdkPayloadException(
                f'Unmanaged error requesting vRa: {e}')

    def get_template(self, catalog_item_id):
        """Get payload template for catalog item request against vRa infrastructure
        
        Args:
            catalog_item_id (string): id of the catalog item
        
        Returns:
            dict: payload of the request to perform to request the specified catalog item
        """

        try:
            req = self.config.session.get(
                f"https://{self.config.vcac_server}/catalog-service/api/consumer/entitledCatalogItems/{catalog_item_id}/requests/template",
                verify=self.config.verify,
                timeout=self.config.timeout)
            req.raise_for_status()
            return json.loads(req.text) 
        except requests.exceptions.RequestException as e:
            raise VraSdkRequestException(
                f'vRa request exception : {e}')
        except Exception as e:
            raise VraSdkPayloadException(
                f'Unmanaged error requesting vRa: {e}')
        

class ResourceAction(BasePayload):
    def __init__(self, customization_func=None, **kwargs):
        """Init ResourceAction object for vRa 7.x payload object
            customization_func ([type], optional): Defaults to None. If not None, this function will add a second customization after the initial one.
        """

        super().__init__()
        self.customized = None
        if not kwargs.get('payload_path'):
            self.base = self.get_template(kwargs.get('resource_id'), kwargs.get('resource_action_id'))
        else:
            self.base = load_payload_file(kwargs['payload_path'])

        self.customized = self.customize_payload(deepcopy(self.base), **kwargs)
        if customization_func:
            self.customized = customization_func(self.customized, **kwargs)

    def execute_request(self):
        """Execute the request against the vRa infrastructure
        
        Returns:
            requests.Request: request object
        """

        try:
            req = self.config.session.post(
                f"https://{self.config.vcac_server}/catalog-service/api/consumer/resources/{self.customized['resourceId']}/actions/{self.customized['actionId']}/requests",
                json=self.customized,
                verify=self.config.verify,
                timeout=self.config.timeout)
            req.raise_for_status()
            return req
        except requests.exceptions.RequestException as e:
            raise VraSdkRequestException(
                f'vRa request exception : {e}')
        except Exception as e:
            raise VraSdkPayloadException(
                f'Unmanaged error requesting vRa: {e}')

    def get_template(self, resource_id, resource_action_id):
        """Get payload template for resource action request against vRa infrastructure
        
        Args:
            resource_id (string): id of the resource to perform the action on
            resource_action_id (string): id of the action to perform
        
        Returns:
            dict: payload of the request to perform to request the specified action on the specified resource
        """

        try:
            req = self.config.session.get(
                f"https://{self.config.vcac_server}/catalog-service/api/consumer/resources/{resource_id}/actions/{resource_action_id}/requests/template",
                verify=self.config.verify,
                timeout=self.config.timeout)
            req.raise_for_status()
            return json.loads(req.text)
        except requests.exceptions.RequestException as e:
            raise VraSdkRequestException(
                f'vRa request exception : {e}')
        except Exception as e:
            raise VraSdkPayloadException(
                f'Unmanaged error requesting vRa: {e}')
