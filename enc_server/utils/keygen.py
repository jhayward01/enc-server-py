from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import enc_server


class Cipher:
    def __init__(self, key: bytes, nonce: bytes):
        self.key = key
        self.nonce = nonce
        self.aesgcm = AESGCM(self.key)

    def encrypt(self, s: str) -> str:
        data = s.encode('utf-8')
        enc = self.aesgcm.encrypt(self.nonce, data, None)
        return enc.hex()

    def decrypt(self, s: str) -> str:
        data = bytes.fromhex(s)
        dec = self.aesgcm.decrypt(self.nonce, data, None)
        return dec.decode('utf-8')


class Keygen:
    def __init__(self, configs: dict):
        result, missing = enc_server.utils.ConfigFile.verify_configs(configs, ["keySize", "idNonceStr"])
        if not result:
            raise KeyError("Keygen missing configuration " + missing)

        self.key_size = int(configs["keySize"]) * 8
        self.nonce = configs["idNonceStr"].encode('utf-8')

    def random_key(self) -> bytes:
        return AESGCM.generate_key(self.key_size)
