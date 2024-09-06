import enc_server
import unittest


class ConnTestSuite(unittest.TestCase):
    record_id = "JTH"
    record_payload = "PAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADS"

    mongo_uri = "mongodb://localhost:27017/"
    db = enc_server.utils.DB({"mongoURI": mongo_uri})

    def test_init(self):
        self.assertIsNotNone(ConnTestSuite.db)

    def test_store_record(self):
        self.assertIsNone(ConnTestSuite.db.store_record(ConnTestSuite.record_id, ConnTestSuite.record_payload))

    def test_retrieve_record(self):
        self.test_store_record()
        record_payload = ConnTestSuite.db.retrieve_record(ConnTestSuite.record_id)
        self.assertEqual(ConnTestSuite.record_payload, record_payload)

    def test_delete_record(self):
        self.test_store_record()
        self.assertIsNone(ConnTestSuite.db.delete_record(ConnTestSuite.record_id))


if __name__ == '__main__':
    unittest.main()
