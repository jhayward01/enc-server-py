import logging

from enc_server import utils, be


class Server(utils.Responder):
    expected_fields = {"STORE": 3, "RETRIEVE": 3, "DELETE": 3}

    def __init__(self, configs: dict):
        self.keygen = utils.Keygen(configs)
        self.be_client = be.client.Client(configs)
        self.socket_io = utils.SocketIO(configs, self)

    def respond(self, msg: bytes) -> bytes:
        result = bytes
        s = msg.decode('utf-8').strip()
        fields = s.split()
        logging.info(fields)

        if (not fields or fields[0] not in Server.expected_fields or
                len(fields) != Server.expected_fields[fields[0]]):
            result = f"ERROR Malformed request: {s}\n".encode('utf-8')
        elif fields[0] == "STORE":
            result = self.store_record(fields)
        elif fields[0] == "RETRIEVE":
            result = self.retrieve_record(fields)
        elif fields[0] == "DELETE":
            result = self.delete_record(fields)

        logging.info(result)
        return result

    def store_record(self, fields: list) -> bytes:
        try:
            key = self.keygen.random_key()
            cipher = utils.Cipher(key, self.keygen.nonce)
            record_id_enc = cipher.encrypt(fields[1])
            record_payload_enc = cipher.encrypt(fields[2])
            self.be_client.store(record_id_enc, record_payload_enc)
            key_str = key.hex()
        except RuntimeError as err:
            return f"ERROR: {err}\n".encode('utf-8')
        else:
            return f"{key_str}\n".encode('utf-8')

    def retrieve_record(self, fields: list) -> bytes:
        try:
            key = bytes.fromhex(fields[2])
            cipher = utils.Cipher(key, self.keygen.nonce)
            record_id_enc = cipher.encrypt(fields[1])
            record_payload_enc = self.be_client.retrieve(record_id_enc)
            record_payload = cipher.decrypt(record_payload_enc)
        except RuntimeError as err:
            return f"ERROR: {str(err)}\n".encode('utf-8')
        else:
            return (record_payload + "\n").encode('utf-8')

    def delete_record(self, fields: list) -> bytes:
        try:
            key = bytes.fromhex(fields[2])
            cipher = utils.Cipher(key, self.keygen.nonce)
            record_id_enc = cipher.encrypt(fields[1])
            self.be_client.delete(record_id_enc)
        except RuntimeError as err:
            return f"ERROR: {str(err)}\n".encode('utf-8')
        else:
            return "\n".encode('utf-8')

    def start(self, server_config=False):
        self.socket_io.start(server_config=server_config)
