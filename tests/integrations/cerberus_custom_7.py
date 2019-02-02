from cerberus import Validator
from vra_sdk.vra_decorator import singleton

@singleton
class CerberusCustomValidator7:
    def __init__(self):
        self.validator = Validator()
        self.schema_catalog_item = {
            'type': {
                'type': 'string',
                'allowed': ['com.vmware.vcac.catalog.domain.request.CatalogItemProvisioningRequest'],
                'required': True
            },
            'catalogItemId': {'type': 'string', 'required': True},
            'businessGroupId': {'type': 'string', 'required': True},
            'description': {'type': 'string'},
            'requestedFor': {'type': 'string'},
            'data': {
                'type': 'dict',
                'required': True,
                'allow_unknown': True
            }
        }
        self.schema_resource_action = {
            'type': {
                'type': 'string',
                'allowed': ['com.vmware.vcac.catalog.domain.request.CatalogResourceRequest'],
                'required': True
            },
            'resourceId': {'type': 'string', 'required': True},
            'actionId': {'type': 'string', 'required': True},
            'description': {'type': 'string'},
            'requestedFor': {'type': 'string'},
            'data': {
                'type': 'dict',
                'required': True,
                'allow_unknown': True
            }
        }

    def catalog_item(self, data):
        return self.payload_validator(data, self.schema_catalog_item)

    def resource_action(self, data):
        return self.payload_validator(data, self.schema_resource_action)

    def payload_validator(self, data, schema):
        return self.validator.validate(data, schema)
