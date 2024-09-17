import logging

from enc_server import utils


class Server(utils.Responder):
    expected_fields = {"STORE": 3, "RETRIEVE": 2, "DELETE": 2}

    def __init__(self, configs: dict):
        self.db = utils.DB(configs)
        self.socket_io = utils.SocketIO(configs, self)

    def respond(self, msg: bytes) -> bytes:
        result = str()
        s = msg.decode('utf-8').strip()
        logging.info(f"BE Server processing '{s}'")
        fields = s.split()

        if (not fields or fields[0] not in Server.expected_fields or
                len(fields) != Server.expected_fields[fields[0]]):
            result = f"ERROR Malformed request: {s}"
        elif fields[0] == "STORE":
            result = self.store_record(fields)
        elif fields[0] == "RETRIEVE":
            result = self.retrieve_record(fields)
        elif fields[0] == "DELETE":
            result = self.delete_record(fields)

        logging.info(f"BE Server returning '{result}'")
        return (result + '\n').encode('utf-8')

    def store_record(self, fields: list) -> str:
        try:
            self.db.store_record(fields[1], fields[2])
        except RuntimeError as err:
            return "ERROR: " + str(err)
        else:
            return "SUCCESS"

    def retrieve_record(self, fields: list) -> str:
        try:
            payload = self.db.retrieve_record(fields[1])
        except RuntimeError as err:
            return f"ERROR: {err}"
        else:
            return payload

    def delete_record(self, fields: list) -> str:
        try:
            self.db.delete_record(fields[1])
        except RuntimeError as err:
            return f"ERROR: {err}"
        else:
            return "SUCCESS"

    def start(self, server_config=False):
        self.socket_io.start(server_config=server_config)
