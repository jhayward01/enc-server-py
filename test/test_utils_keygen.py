import enc_server
import unittest


class KeyGenTestSuite(unittest.TestCase):
    key_size = "32"
    bad_key_size = "Steve"

    record_payload = b"PAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADS"

    def test_init(self):
        self.assertIsNotNone(enc_server.utils.Keygen({"keySize": KeyGenTestSuite.key_size}))

    def test_missing_init(self):
        self.assertRaises(KeyError, enc_server.utils.Keygen, {})

    def test_bad_init(self):
        self.assertRaises(ValueError, enc_server.utils.Keygen, {"keySize": KeyGenTestSuite.bad_key_size})

    def test_enc_dec(self):
        keygen = enc_server.utils.Keygen({"keySize": KeyGenTestSuite.key_size})
        enc_payload = keygen.encrypt(KeyGenTestSuite.record_payload)
        dec_payload = keygen.decrypt(enc_payload)
        self.assertEqual(KeyGenTestSuite.record_payload, dec_payload)


if __name__ == '__main__':
    unittest.main()
