from enc_server import utils, be


class Server(utils.Responder):
    expected_fields = {"STORE": 3, "RETRIEVE": 3, "DELETE": 3}

    def __init__(self, configs: dict):
        self.keygen = utils.Keygen(configs)
        self.be_client = be.client.Client(configs)
        self.socket_io = utils.SocketIO(configs, self)

    def respond(self, msg: bytes) -> bytes:
        s = msg.decode('utf-8').strip()
        fields = s.split()

        if (not fields or fields[0] not in Server.expected_fields or
                len(fields) != Server.expected_fields[fields[0]]):
            return f"ERROR Malformed request: {s}\n".encode('utf-8')

        if fields[0] == "STORE":
            return self.store_record(fields)
        elif fields[0] == "RETRIEVE":
            return self.retrieve_record(fields)
        elif fields[0] == "DELETE":
            return self.delete_record(fields)

    def store_record(self, fields: list) -> bytes:
        try:
            key = self.keygen.random_key()
            cipher = utils.Cipher(key, self.keygen.nonce)
            record_id_enc = cipher.encrypt(fields[1])
            record_payload_enc = cipher.encrypt(fields[2])
            self.be_client.store(record_id_enc, record_payload_enc)
        except RuntimeError as err:
            return f"ERROR: {err}\n".encode('utf-8')
        else:
            return key

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

    def start(self):
        self.socket_io.start()
