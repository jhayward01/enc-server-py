import enc_server
import unittest


class ConnTestSuite(unittest.TestCase):
    record_id = "JTH"
    record_payload = "PAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADS"

    mongo_uri = "mongodb://localhost:27017/"

    def setUp(self):
        self.db = enc_server.utils.DB({"mongoURI": ConnTestSuite.mongo_uri})

    def test_init(self):
        self.assertIsNotNone(self.db)

    def test_db(self):
        self.assertIsNone(self.db.store_record(ConnTestSuite.record_id, ConnTestSuite.record_payload))
        self.assertEqual(ConnTestSuite.record_payload, self.db.retrieve_record(ConnTestSuite.record_id))
        self.assertIsNone(self.db.delete_record(ConnTestSuite.record_id))


if __name__ == '__main__':
    unittest.main()
