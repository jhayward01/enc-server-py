from abc import ABC
import config
import socket


class Responder(ABC):
    def respond(self, msg: bytes) -> bytes:
        pass


class SocketIO:
    buffer_size = 1024
    host = "localhost"

    def __init__(self, configs: dict, responder: Responder):
        result, missing = config.verify_configs(configs, ["port"])
        if not result:
            raise KeyError("Keygen missing configuration " + missing)

        self.port = int(configs["port"])
        self.responder = responder

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((SocketIO.host, self.port))
            server.listen()
            conn, addr = server.accept()
            with conn:
                while True:
                    data = conn.recv(SocketIO.buffer_size)
                    if not data:
                        break
                    conn.sendall(self.responder.respond(data))
