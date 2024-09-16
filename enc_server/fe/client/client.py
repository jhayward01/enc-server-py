import enc_server


class Client:

    def __init__(self, configs: dict):
        self.conn = enc_server.utils.ConnSocket(configs)

    def transmit(self, message: str) -> str:
        try:
            response = self.conn.get_response(message)
            if response.startswith("ERROR"):
                raise RuntimeError(response)
        except Exception as err:
            raise RuntimeError(err) from None
        return response

    def store(self, record_id: str, record_payload: str) -> str:
        return self.transmit(f"STORE {record_id} {record_payload}\n")

    def retrieve(self, record_id: str, key: str) -> str:
        return self.transmit(f"RETRIEVE {record_id} {key}\n")

    def delete(self, record_id: str, key: str) -> str:
        return self.transmit(f"DELETE {record_id} {key}\n")
