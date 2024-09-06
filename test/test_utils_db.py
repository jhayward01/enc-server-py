import enc_server
import unittest


class ConnTestSuite(unittest.TestCase):
    enc_server.utils.get_record_collection()


if __name__ == '__main__':
    unittest.main()
