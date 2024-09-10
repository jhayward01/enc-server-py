import enc_server
import socket
import socketio
import threading
import unittest


class SocketioTestSuite(unittest.TestCase):
    host = "localhost"
    port = 7777
    buffer_size = 1024

    msg = b"Hi"
    response = b"Hello"

    class TestResponder(socketio.Responder):
        def respond(self, msg: bytes) -> bytes:
            return SocketioTestSuite.response

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

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SocketioTestSuite.host, SocketioTestSuite.port))
            s.sendall(SocketioTestSuite.msg)
            response = s.recv(SocketioTestSuite.buffer_size)
            self.assertEqual(SocketioTestSuite.response, response)

        server.join()
