import config
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Cipher:
    def __init__(self, configs: dict):
        result, missing = config.verify_configs(configs, ["key", "nonce"])
        if not result:
            raise KeyError("Keygen missing configuration " + missing)

        self.key = configs["key"]
        self.nonce = configs["nonce"]

        self.aesgcm = AESGCM(self.key)

    def encrypt(self, data: bytes) -> bytes:
        return self.aesgcm.encrypt(self.nonce, data, None)

    def decrypt(self, data: bytes) -> bytes:
        return self.aesgcm.decrypt(self.nonce, data, None)


class Keygen:
    def __init__(self, configs: dict):
        result, missing = config.verify_configs(configs, ["keySize"])
        if not result:
            raise KeyError("Keygen missing configuration " + missing)

        self.key_size = int(configs["keySize"]) * 8
        self.nonce_size = 12

    def random_key(self):
        return AESGCM.generate_key(self.key_size)

    def random_nonce(self):
        return os.urandom(self.nonce_size)
