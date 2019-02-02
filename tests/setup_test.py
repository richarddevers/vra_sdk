# -*- coding: utf-8 -*-

import unittest
from vra_sdk.vra_config import VraConfig


class SetupTest(unittest.TestCase):
    def teardown_method(self, methodf):
        config = VraConfig()
        config._sealed = False
