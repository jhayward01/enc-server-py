import enc_server
import unittest


class KeyGenTestSuite(unittest.TestCase):
    key_size = "32"
    bad_key_size = "Steve"

    def test_init(self):
        self.assertIsNotNone(enc_server.utils.Keygen({"keySize": KeyGenTestSuite.key_size}))

    def test_missing_init(self):
        self.assertRaises(KeyError, enc_server.utils.Keygen, {})

    def test_bad_init(self):
        self.assertRaises(ValueError, enc_server.utils.Keygen, {"keySize": KeyGenTestSuite.bad_key_size})


if __name__ == '__main__':
    unittest.main()
