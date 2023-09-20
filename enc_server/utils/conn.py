import abc
import socket


class ConnInterface(abc.ABC):
    @abc.abstractmethod
    def get_response(self, message: str) -> str:
        pass


class ConnSocket(ConnInterface):

    buffer_size = 1024

    def __init__(self, server_addr):
        self.server_host = server_addr.split(":")[0]
        self.server_port = int(server_addr.split(":")[1])

    def get_response(self, message: str) -> str:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            s.sendall(bytes(message, 'utf-8'))
            data = s.recv(ConnSocket.buffer_size)

        return str(data, 'utf-8').splitlines()[0]
