import logging
import socket

import enc_server


class ConnSocket:
    buffer_size = 1024

    def __init__(self, configs: dict):
        result, missing = enc_server.utils.ConfigFile.verify_configs(configs, ["serverAddr"])
        if not result:
            raise KeyError("ConnSocket missing configuration " + missing)

        server_addr = configs["serverAddr"]
        self.server_host = server_addr.split(":")[0]
        self.server_port = int(server_addr.split(":")[1])

    def get_response(self, message: str) -> str:
        logging.debug(f"Transmitting {message.strip()}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            s.sendall(bytes(message, 'utf-8'))
            data = s.recv(ConnSocket.buffer_size)

        response = data.decode('utf-8').strip()
        logging.debug(f"Received {response}")
        return response
