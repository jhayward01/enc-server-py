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

        self.key = AESGCM.generate_key(self.key_size*8)
        self.nonce = os.urandom(self.nonce_size)

        self.aesgcm = AESGCM(self.key)

    def encrypt(self, data: bytes) -> bytes:
        return self.aesgcm.encrypt(self.nonce, data, None)

    def decrypt(self, data: bytes) -> bytes:
        return self.aesgcm.decrypt(self.nonce, data, None)
