import socket
import threading
import unittest

import enc_server


class BEClientTestSuite(unittest.TestCase):
    server_addr = "localhost:8888"
    bad_server_addr = "foobar"
    buffer_size = 1024

    record_id_enc = "396263343233393039616335acc30dd405c51d37675d4e0002a526ae113d56"

    record_payload_enc = ("396263343233393039616335b6d61c6839a0dda2524d19b4e5d" +
                          "ac5a1fda8902ad2701ced5c31c89088c3151d039ee27d003b75c3a140141c05da496572142eb" +
                          "5466c5edb07de33d8ac301f19789fbef68e5c3f280bf4f274e8d2d2d7")

    def setUp(self):
        self.client = enc_server.be.client.Client({"serverAddr": BEClientTestSuite.server_addr})

    def test_init(self):
        self.assertIsNotNone(self.client)

    def test_bad_init(self):
        self.assertRaises(KeyError, enc_server.be.client.Client, {})

    def test_error(self):
        server = threading.Thread(target=BEClientTestSuite.socket_server)
        server.start()

        self.assertRaises(RuntimeError, self.client.transmit, "FOO\n")

        server.join()

    def test_store(self):
        server = threading.Thread(target=BEClientTestSuite.socket_server)
        server.start()

        store_response = self.client.store(BEClientTestSuite.record_id_enc, BEClientTestSuite.record_payload_enc)
        self.assertEqual("SUCCESS", store_response)

        server.join()

    def test_retrieve(self):
        server = threading.Thread(target=BEClientTestSuite.socket_server)
        server.start()

        retrieve_response = self.client.retrieve(BEClientTestSuite.record_id_enc)
        self.assertEqual(BEClientTestSuite.record_payload_enc, retrieve_response)

        server.join()

    def test_delete(self):
        server = threading.Thread(target=BEClientTestSuite.socket_server)
        server.start()

        delete_response = self.client.delete(BEClientTestSuite.record_id_enc)
        self.assertEqual("", delete_response)

        server.join()

    @staticmethod
    def socket_server():
        server_host = BEClientTestSuite.server_addr.split(":")[0]
        server_port = int(BEClientTestSuite.server_addr.split(":")[1])

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((server_host, server_port))
            server.listen()
            conn, addr = server.accept()
            with conn:
                while True:
                    data = conn.recv(BEClientTestSuite.buffer_size)
                    if not data:
                        break
                    message, response = data.decode('utf-8').strip(), str()
                    if message == f"STORE {BEClientTestSuite.record_id_enc} {BEClientTestSuite.record_payload_enc}":
                        response = "SUCCESS\n"
                    elif message == f"RETRIEVE {BEClientTestSuite.record_id_enc}":
                        response = f"{BEClientTestSuite.record_payload_enc}\n"
                    elif message == f"DELETE {BEClientTestSuite.record_id_enc}":
                        response = "\n"
                    else:
                        response = "ERROR\n"
                    conn.sendall(response.encode('utf-8'))
