# -*- coding: UTF-8 -*-
import os
from app import app
from . import logger
import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def begin(self, method, string):
        if method:
            logger.info("TEST API: "+method+" "+string)
        else:
            logger.info("TEST: "+string)
        print ("\n\n%s\n====================\t%s\t====================" % (method, string))

    def tearDown(self):
        logger.info("TEST DONE")
        print("====================\tTest Done\t====================\n")
