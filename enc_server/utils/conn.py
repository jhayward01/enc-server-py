import abc


class ConnInterface(abc.ABC):
    @abc.abstractmethod
    def get_response(self, message: str) -> str:
        pass


class ConnSocket(ConnInterface):
    server_host = str()
    server_port = str()

    def __init__(self, server_addr):
        self.server_host = server_addr.split(":")[0]
        self.server_port = server_addr.split(":")[1]

    def get_response(self, message: str) -> str:
        pass
