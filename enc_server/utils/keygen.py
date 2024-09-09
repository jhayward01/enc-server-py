import config
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class Keygen:

    def __init__(self, configs: dict):
        result, missing = config.verify_configs(configs, ["keySize"])
        if not result:
            raise KeyError("Keygen missing configuration " + missing)

        self.key_size = int(configs["keySize"])
        self.nonce_size = 12

    def random_key(self) -> bytes:
        return AESGCM.generate_key(key_size=self.key_size)

    def random_nonce(self) -> bytes:
        return os.urandom(self.nonce_size)

    @staticmethod
    def encrypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
        aesgcm = AESGCM(key)
        return aesgcm.encrypt(nonce, data, None)

    @staticmethod
    def decrypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, data, None)
