import logging
import socket
import time
from abc import ABC

import enc_server


class Responder(ABC):
    def respond(self, msg: bytes) -> bytes:
        pass


class SocketIO:
    buffer_size = 1024

    def __init__(self, configs: dict, responder: Responder):
        result, missing = enc_server.utils.ConfigFile.verify_configs(configs, ["port", "useExtIP"])
        if not result:
            raise KeyError("SocketIO missing configuration " + missing)

        self.host = socket.gethostbyname(socket.gethostname()) if configs["useExtIP"] == "True" else "localhost"
        self.port = int(configs["port"])
        self.responder = responder

    def start(self, server_config=False):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                logging.debug(f"Binding to {self.host} port {self.port}")
                server.bind((self.host, self.port))
                server.listen()
                conn, addr = server.accept()
                logging.debug(f"Accepted connection from {addr[0]} port {addr[1]}")
                with conn:
                    while True:
                        data = conn.recv(SocketIO.buffer_size)
                        if not data:
                            break
                        conn.sendall(self.responder.respond(data))
            if not server_config:
                return
            time.sleep(1)
