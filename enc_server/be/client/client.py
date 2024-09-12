from enc_server import utils


class Client:

    def __init__(self, configs: dict):
        self.conn = utils.ConnSocket(configs)

    def transmit(self, message:str):
        response = self.conn.get_response(message)
        if response.startswith("ERROR"):
            raise RuntimeError(response)
        return response

    def store(self, record_id: str, record_payload: str):
        return self.transmit(f"STORE {record_id} {record_payload}\n")

    def retrieve(self, record_id: str) -> str:
        return self.transmit(f"RETRIEVE {record_id}\n")

    def delete(self, record_id: str) -> str:
        return self.transmit(f"DELETE {record_id}\n")
