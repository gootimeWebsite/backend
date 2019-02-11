import os
from app import app
import unittest


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def begin(self, method, string):
        print ("\n\n%s\n====================\tTest:%s\t====================" % (method, string))

    def tearDown(self):
        print("====================\tTest Done\t====================\n")
