# -*- coding: utf-8 -*-
from vra_sdk.models.vra_object import VraBaseObject

RESOURCE_TYPE = ['Virtual Machine']


class Vm(VraBaseObject):

    def __init__(self, raw_data=None, id=None, name=None, attr1=None, attr2=None):

        super().__init__()

        self.raw_data = raw_data
        self.id = id
        self.name = name
        self.attr1 = attr1 or []
        self.attr2 = attr2 or []
