from cerberus import Validator
from vra_sdk.vra_decorator import singleton


@singleton
class CerberusCustomValidator6:
    def __init__(self):
        self.validator = Validator()

        self.schema_catalog_item = {
            '@type': {
                'type': 'string',
                'allowed': ['CatalogItemRequest'],
                'required': True
            },
            'catalogItemRef': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'id': {
                        'type': 'string',
                        'required': True
                    }
                }
            },
            'organization': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'tenantRef': {
                        'type': 'string',
                        'required': True
                    },
                    'subtenantRef': {
                        'type': 'string',
                        'required': True
                    },
                    'tenantLabel': {
                        'type': 'string',
                        'required': True
                    },
                    'subtenantLabel': {
                        'type': 'string',
                        'required': True
                    }
                }
            },
            'requestedFor': {
                'type': 'string',
                'required': True
            },
            'requestNumber': {
                'type': 'integer',
                'required': True
            },
            'state': {
                'type': 'string',
                'required': True,
                'allowed': ['SUBMITTED']
            },
            'requestData': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'entries': {
                        'type': 'list',
                        'required': True,
                        'allow_unknown': True
                    }
                }
            }
        }

        self.schema_resource_action = {
            '@type': {
                'type': 'string',
                'allowed': ['ResourceActionRequest'],
                'required': True
            },
            'organization': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'tenantRef': {
                        'type': 'string',
                        'required': True
                    },
                    'subtenantRef': {
                        'type': 'string',
                        'required': True
                    },
                    'tenantLabel': {
                        'type': 'string',
                        'required': True
                    },
                    'subtenantLabel': {
                        'type': 'string',
                        'required': True
                    }
                }
            },
            'requestNumber': {
                'required': True,
                'type': 'integer'
            },
            'resourceActionRef': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'id': {
                        'type': 'string',
                        'required': True
                    }
                }
            },
            'resourceRef': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'id': {
                        'type': 'string',
                        'required': True
                    }
                }
            },
            'state':{
                'type':'string',
                'required':True,
                'allowed':['SUBMITTED']
            },
            'requestData': {
                'required': True,
                'type': 'dict',
                'schema': {
                    'entries': {
                        'type': 'list',
                        'required': True,
                        'allow_unknown': True
                    }
                }
            }
        }

    def catalog_item(self, data):
        return self.payload_validator(data, self.schema_catalog_item)

    def resource_action(self, data):
        return self.payload_validator(data, self.schema_resource_action)

    def payload_validator(self, data, schema):
        return self.validator.validate(data, schema)
