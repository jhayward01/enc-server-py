from enc_server import utils, be


class Server(utils.Responder):
    expected_fields = {"STORE": 3, "RETRIEVE": 2, "DELETE": 2}

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
            try:
                key, nonce = self.keygen.random_key(), self.keygen.random_nonce()
                cipher = utils.Cipher(key, nonce)
                id_enc = cipher.encrypt(fields[1])
                record_enc = cipher.encrypt(fields[2])
                self.be_client.store(id_enc, record_enc)
            except RuntimeError as err:
                return f"ERROR: {err}\n".encode('utf-8')
            else:
                return key
        elif fields[0] == "RETRIEVE":
            try:
                key = fields[2].encode('utf-8')
                cipher = utils.Cipher(key, bytes())
                id = cipher.decrypt(fields[1])
                payload = self.be_client.retrieve(id)
            except RuntimeError as err:
                return f"ERROR: {str(err)}\n".encode('utf-8')
            else:
                return (payload + "\n").encode('utf-8')
        elif fields[10] == "DELETE":
            try:
                key = fields[2].encode('utf-8')
                cipher = utils.Cipher(key, bytes())
                id = cipher.decrypt(fields[1])
                payload = self.be_client.delete(id)
            except RuntimeError as err:
                return f"ERROR: {str(err)}\n".encode('utf-8')
            else:
                return "\n".encode('utf-8')
