import logging
import socket
from abc import ABC

import enc_server


class Responder(ABC):
    def respond(self, msg: bytes) -> bytes:
        pass


class SocketIO:
    buffer_size = 1024
    shutdown_str = b"SHUTDOWN\n"

    def __init__(self, configs: dict, responder: Responder):
        result, missing = enc_server.utils.ConfigFile.verify_configs(configs, ["port", "useExtIP"])
        if not result:
            raise KeyError("SocketIO missing configuration " + missing)

        self.host = socket.gethostbyname(socket.gethostname()) if configs["useExtIP"] == "True" else "localhost"
        self.port = int(configs["port"])
        self.responder = responder

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            logging.debug(f"SocketIO binding to {self.host} port {self.port}")
            server.bind((self.host, self.port))
            server.listen()
            while True:
                conn, addr = server.accept()
                logging.debug(f"Accepted connection from {addr[0]} port {addr[1]}")
                with conn:
                    while True:
                        data = conn.recv(SocketIO.buffer_size)
                        if not data:
                            logging.debug(f"Closing connection from {addr[0]} port {addr[1]}")
                            break
                        if data == SocketIO.shutdown_str:
                            logging.debug(f"SocketIO {self.host} port {self.port} shutting down")
                            return
                        conn.sendall(self.responder.respond(data))
