# -*- coding: utf-8 -*-
from vra_sdk.models.vra_object import VraBaseObject


class FakeObject(VraBaseObject):
    def __init__(self, fake_attr1=None, fake_attr2=None, fake_attr_empty=None):
        super().__init__()

        self.fake_attr1 = fake_attr1
        self.fake_attr2 = fake_attr2
        self.fake_attr_empty = fake_attr_empty
