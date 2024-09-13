import enc_server
import unittest


class KeyGenTestSuite(unittest.TestCase):
    key_size = "32"
    bad_key_size = "Steve"

    record_payload = "PAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADS"

    def setUp(self):
        self.keygen = enc_server.utils.Keygen({"keySize": KeyGenTestSuite.key_size})
        self.key, self.nonce = self.keygen.random_key(), self.keygen.random_nonce()
        self.cipher = enc_server.utils.Cipher(self.key, self.nonce)

    def test_init(self):
        self.assertIsNotNone(self.keygen)
        self.assertIsNotNone(self.key)
        self.assertIsNotNone(self.nonce)
        self.assertIsNotNone(self.cipher)

    def test_missing_init(self):
        self.assertRaises(KeyError, enc_server.utils.Keygen, {})

    def test_enc_dec(self):
        enc_payload = self.cipher.encrypt(KeyGenTestSuite.record_payload)
        dec_payload = self.cipher.decrypt(enc_payload)
        self.assertEqual(KeyGenTestSuite.record_payload, dec_payload)
