import logging
import socket
import threading
import time
import unittest

import enc_server


class ConnTestSuite(unittest.TestCase):
    server_host = "localhost"
    server_port = 7777
    server_addr = f"{server_host}:{server_port}"

    bad_server_addr = "foobar"

    buffer_size = 1024
    server_msg = "Hi"
    server_response = "Hello"

    def test_init(self):
        conn = enc_server.utils.ConnSocket({"serverAddr": ConnTestSuite.server_addr})
        self.assertIsNotNone(conn)

    def test_init_err(self):
        self.assertRaises(IndexError, enc_server.utils.ConnSocket,
                          {"serverAddr": ConnTestSuite.bad_server_addr})

    def test_get_response(self):
        server = threading.Thread(target=ConnTestSuite.socket_server)
        server.start()
        time.sleep(1)

        conn = enc_server.utils.ConnSocket({"serverAddr": ConnTestSuite.server_addr})
        response = conn.get_response(ConnTestSuite.server_msg)
        self.assertEqual(response, ConnTestSuite.server_response)

        server.join()

    def test_get_response_err(self):
        conn = enc_server.utils.ConnSocket({"serverAddr": ConnTestSuite.server_addr})
        self.assertRaises(ConnectionRefusedError, conn.get_response,
                          ConnTestSuite.server_msg)

    @staticmethod
    def socket_server():

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            logging.info(f"Binding to {ConnTestSuite.server_host} port {ConnTestSuite.server_port}")
            server.bind((ConnTestSuite.server_host, ConnTestSuite.server_port))
            server.listen()
            conn, addr = server.accept()
            logging.info(f"Accepted connection from {addr[0]} port {addr[1]}")
            with conn:
                while True:
                    data = conn.recv(ConnTestSuite.buffer_size)
                    if not data:
                        break
                    conn.sendall(bytes(ConnTestSuite.server_response, 'utf-8'))
