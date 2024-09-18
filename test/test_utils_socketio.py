import logging
import socket
import threading
import time
import unittest

import enc_server


class SocketioTestSuite(unittest.TestCase):
    host = "localhost"
    port = 7780
    buffer_size = 1024

    msg = "Hi\n"
    response = "Hello\n"

    def setUp(self):
        self.responder = SocketioTestSuite.TestResponder()
        self.socket_io = enc_server.utils.SocketIO({"port": SocketioTestSuite.port}, self.responder)

    def test_init(self):
        self.assertIsNotNone(self.responder)
        self.assertIsNotNone(self.socket_io)

    def test_missing_init(self):
        self.assertRaises(KeyError, enc_server.utils.SocketIO, {}, None)

    def test_get_response(self):
        server = threading.Thread(target=self.socket_io.start)
        server.start()
        time.sleep(1)

        logging.info(f"Transmitting {SocketioTestSuite.msg.strip()}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SocketioTestSuite.host, SocketioTestSuite.port))
            s.sendall(SocketioTestSuite.msg.encode('utf-8'))
            data = s.recv(SocketioTestSuite.buffer_size)

        response = data.decode('utf-8')
        logging.info(f"Received {response}")
        self.assertEqual(SocketioTestSuite.response, response)

        server.join()

    class TestResponder(enc_server.utils.socketio.Responder):
        def respond(self, msg: bytes) -> bytes:
            return SocketioTestSuite.response.encode('utf-8')
