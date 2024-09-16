from enc_server import utils


class Server(utils.Responder):
    expected_fields = {"STORE": 3, "RETRIEVE": 2, "DELETE": 2}

    def __init__(self, configs: dict):
        self.db = utils.DB(configs)
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
            self.db.store_record(fields[1], fields[2])
        except RuntimeError as err:
            return ("ERROR: " + str(err) + "\n").encode('utf-8')
        else:
            return "SUCCESS\n".encode('utf-8')

    def retrieve_record(self, fields: list) -> bytes:
        try:
            payload = self.db.retrieve_record(fields[1])
        except RuntimeError as err:
            return f"ERROR: {str(err)}\n".encode('utf-8')
        else:
            return (payload + "\n").encode('utf-8')

    def delete_record(self, fields: list) -> bytes:
        try:
            self.db.delete_record(fields[1])
        except RuntimeError as err:
            return f"ERROR: {str(err)}\n".encode('utf-8')
        else:
            return "\n".encode('utf-8')

    def start(self, server_config=False):
        self.socket_io.start(server_config=server_config)
