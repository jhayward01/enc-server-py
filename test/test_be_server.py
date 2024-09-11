import enc_server
import unittest


class ConfigTestSuite(unittest.TestCase):

    configs = {'port': '8888', 'mongoURI': 'mongodb://user:pass@mongodb'}

    def test_init(self):
        self.assertIsNotNone(enc_server.be.server.Server(ConfigTestSuite.configs))
