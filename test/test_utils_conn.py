import enc_server
import unittest


class ConnTestSuite(unittest.TestCase):
    server_addr = "localhost:7777"
    bad_server_addr = "foobar"

    def test_init(self):
        conn = enc_server.utils.ConnSocket(ConnTestSuite.server_addr)
        self.assertIsNotNone(conn)

    def test_init_err(self):
        self.assertRaises(IndexError, enc_server.utils.ConnSocket,
                          ConnTestSuite.bad_server_addr)


if __name__ == '__main__':
    unittest.main()
