from enc_server import utils


class Server(utils.Responder):

    def __init__(self, configs: dict):
        self.db = utils.DB(configs)
        self.socket_io = utils.SocketIO(configs, self)

    def respond(self, msg: bytes) -> bytes:
        pass
