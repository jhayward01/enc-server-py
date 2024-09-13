import enc_server
import unittest


class FEServerTestSuite(unittest.TestCase):
    configs = {'port': '7777', 'keySize': 32, 'idNonceStr': '9bc423909ac5', 'serverAddr': 'localhost:8888'}
    bad_configs = {'port': '7777', 'keySize': 32, 'idNonceStr': '9bc423909ac5', 'serverAddr': 'localhost:1111'}

    record_id = 'JTH'
    record_payload = 'PAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADS'

    class ClientStub:
        record_payload = str()

        @staticmethod
        def store(record_id: str, record_payload: str) -> str:
            FEServerTestSuite.ClientStub.record_payload = record_payload
            return "SUCCESS\n"

        @staticmethod
        def retrieve(record_id: str) -> str:
            return f"{FEServerTestSuite.ClientStub.record_payload}\n"

        @staticmethod
        def delete(record_id: str) -> str:
            return "\n"

    def test_init(self):
        self.assertIsNotNone(enc_server.fe.server.Server(FEServerTestSuite.configs))

    def test_bad_init(self):
        self.assertRaises(KeyError, enc_server.fe.server.Server, {})

    def test_empty_msg(self):
        server = enc_server.fe.server.Server(FEServerTestSuite.configs)

        empty_message = f"\n".encode('utf-8')
        empty_response = server.respond(empty_message)
        self.assertTrue(empty_response.decode('utf-8').strip().startswith("ERROR Malformed"))

    def test_unknown_msg(self):
        server = enc_server.fe.server.Server(FEServerTestSuite.configs)

        unknown_message = f"FOO\n".encode('utf-8')
        unknown_response = server.respond(unknown_message)
        self.assertTrue(unknown_response.decode('utf-8').strip().startswith("ERROR Malformed"))

    def test_bad_store(self):
        server = enc_server.fe.server.Server(FEServerTestSuite.bad_configs)

        store_message = f"STORE {FEServerTestSuite.id} {FEServerTestSuite.record_payload}\n".encode('utf-8')
        store_response = server.respond(store_message)
        self.assertTrue(store_response.decode('utf-8').strip().startswith("ERROR"))

    def test_db(self):
        server = enc_server.fe.server.Server(FEServerTestSuite.configs)
        server.be_client = FEServerTestSuite.ClientStub()

        store_message = f"STORE {FEServerTestSuite.record_id} {FEServerTestSuite.record_payload}\n".encode(
            'utf-8')
        store_response = server.respond(store_message)
        self.assertIsNotNone(store_response)

        key = store_response.hex()

        retrieve_message = f"RETRIEVE {FEServerTestSuite.record_id} {key}\n".encode('utf-8')
        retrieve_response = server.respond(retrieve_message)
        self.assertEqual(FEServerTestSuite.record_payload, retrieve_response.decode('utf-8').strip())

        delete_message = f"DELETE {FEServerTestSuite.record_id} {key}\n".encode('utf-8')
        delete_response = server.respond(delete_message)
        self.assertEqual("", delete_response.decode('utf-8').strip())
