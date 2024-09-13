import enc_server
import socket
import threading
import unittest


class ConnTestSuite(unittest.TestCase):
    server_addr = "localhost:7777"
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
        server_host = ConnTestSuite.server_addr.split(":")[0]
        server_port = int(ConnTestSuite.server_addr.split(":")[1])

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((server_host, server_port))
            server.listen()
            conn, addr = server.accept()
            with conn:
                while True:
                    data = conn.recv(ConnTestSuite.buffer_size)
                    if not data:
                        break
                    conn.sendall(bytes(ConnTestSuite.server_response, 'utf-8'))
