import logging
import socket
import threading
import time
import unittest

import enc_server


class FEClientTestSuite(unittest.TestCase):
    server_host = "localhost"
    server_port = 7779
    bad_server_addr = "foobar"
    buffer_size = 1024

    record_id = "JTH"
    record_payload = "PAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADS"
    record_payload_enc = ("396263343233393039616335b6d61c6839a0dda2524d19b4e5d" +
                          "ac5a1fda8902ad2701ced5c31c89088c3151d039ee27d003b75c3a140141c05da496572142eb" +
                          "5466c5edb07de33d8ac301f19789fbef68e5c3f280bf4f274e8d2d2d7")
    record_key = "06f1be76f38d296ddb8070dc74e37327970ffee6fad1a8ecc9b9145eedd0c3df"

    def setUp(self):
        self.client = enc_server.fe.client.Client(
            {"serverAddr": f"{FEClientTestSuite.server_host}:{FEClientTestSuite.server_port}"})

    def test_init(self):
        self.assertIsNotNone(self.client)

    def test_store(self):
        server = threading.Thread(target=FEClientTestSuite.socket_server)
        server.start()
        time.sleep(1)

        store_response = self.client.store(FEClientTestSuite.record_id, FEClientTestSuite.record_payload)
        self.assertEqual(FEClientTestSuite.record_key, store_response)

        server.join()

    def test_retrieve(self):
        server = threading.Thread(target=FEClientTestSuite.socket_server)
        server.start()
        time.sleep(1)

        retrieve_response = self.client.retrieve(FEClientTestSuite.record_id, FEClientTestSuite.record_key)
        self.assertEqual(FEClientTestSuite.record_payload, retrieve_response)

        server.join()

    def test_delete(self):
        server = threading.Thread(target=FEClientTestSuite.socket_server)
        server.start()
        time.sleep(1)

        delete_response = self.client.delete(FEClientTestSuite.record_id, FEClientTestSuite.record_key)
        self.assertEqual("SUCCESS", delete_response)

        server.join()

    @staticmethod
    def socket_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            logging.info(f"Binding to {FEClientTestSuite.server_host} port {FEClientTestSuite.server_port}")
            server.bind((FEClientTestSuite.server_host, FEClientTestSuite.server_port))
            server.listen()
            conn, addr = server.accept()
            logging.info(f"Accepted connection from {addr[0]} port {addr[1]}")
            with conn:
                while True:
                    data = conn.recv(FEClientTestSuite.buffer_size)
                    if not data:
                        break
                    message, response = data.decode('utf-8').strip(), str()
                    if message == f"STORE {FEClientTestSuite.record_id} {FEClientTestSuite.record_payload}":
                        response = f"{FEClientTestSuite.record_key}\n"
                    elif message == f"RETRIEVE {FEClientTestSuite.record_id} {FEClientTestSuite.record_key}":
                        response = f"{FEClientTestSuite.record_payload}\n"
                    elif message == f"DELETE {FEClientTestSuite.record_id} {FEClientTestSuite.record_key}":
                        response = "SUCCESS\n"
                    else:
                        response = "ERROR\n"
                    conn.sendall(response.encode('utf-8'))
