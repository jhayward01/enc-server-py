import enc_server
import unittest


class ConfigTestSuite(unittest.TestCase):
    config_path = "../config/config.yaml"
    bad_config_path = ""

    config_map = {
        'feClientConfigs': {'serverAddr': 'localhost:7777'},
        'feServerConfigs': {'keySize': '32', 'idKeyStr': 'vkAZAarLbZ6w0kmL2HJP3eU1ODCgVj4k',
                            'idNonceStr': '9bc423909ac5', 'port': '7777'},
        'beServerConfigs': {'port': '8888', 'mongoURI': 'mongodb://user:pass@mongodb'},
        'beClientConfigs': {'serverAddr': 'enc-server-go-be:8888'},
        'testParams': {'id': 'JTH', 'record': 'PAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADS'}
    }

    config_fields = ['feClientConfigs', 'feServerConfigs', 'beServerConfigs',
                     'beClientConfigs', 'testParams']
    bad_config_fields = ['foo', 'bar']

    def test_load_configs(self):
        loaded_map = enc_server.utils.load_configs(ConfigTestSuite.config_path)
        self.assertEqual(loaded_map, ConfigTestSuite.config_map)

    def test_load_configs_err(self):
        self.assertRaises(FileNotFoundError, enc_server.utils.load_configs,
                          ConfigTestSuite.bad_config_path)

    def test_verify_configs(self):
        result, missing = enc_server.utils.verify_configs(ConfigTestSuite.config_map,
                                                          ConfigTestSuite.config_fields)
        self.assertTrue(result)
        self.assertEqual(missing, "")

    def test_verify_configs_err(self):
        result, missing = enc_server.utils.verify_configs(ConfigTestSuite.config_map,
                                                          ConfigTestSuite.bad_config_fields)
        self.assertFalse(result)
        self.assertEqual(missing, "foo")
