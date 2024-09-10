import enc_server
import unittest


class KeyGenTestSuite(unittest.TestCase):
    key_size = "32"
    bad_key_size = "Steve"

    record_payload = b"PAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADS"

    def setUp(self):
        self.keygen = enc_server.utils.Keygen({"keySize": KeyGenTestSuite.key_size})
        self.key, self.nonce = self.keygen.random_key(), self.keygen.random_nonce()
        self.cipher = enc_server.utils.Cipher({"key": self.key, "nonce": self.nonce})

    def test_init(self):
        self.assertIsNotNone(self.keygen)
        self.assertIsNotNone(self.key)
        self.assertIsNotNone(self.nonce)
        self.assertIsNotNone(self.cipher)

    def test_missing_init(self):
        self.assertRaises(KeyError, enc_server.utils.Keygen, {})
        self.assertRaises(KeyError, enc_server.utils.Cipher, {})

    def test_enc_dec(self):
        enc_payload = self.cipher.encrypt(KeyGenTestSuite.record_payload)
        dec_payload = self.cipher.decrypt(enc_payload)
        self.assertEqual(KeyGenTestSuite.record_payload, dec_payload)


if __name__ == '__main__':
    unittest.main()
