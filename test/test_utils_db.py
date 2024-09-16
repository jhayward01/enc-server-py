import unittest

import enc_server


class DbTestSuite(unittest.TestCase):
    record_id = "JTH"
    record_payload = "PAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADSPAYLOADS"

    mongo_uri = "mongodb://localhost:27017/?timeoutMS=200"
    bad_mongo_uri = "foo://foohost:27017/?timeoutMS=200"

    def setUp(self):
        self.db = None

    def setup_db(self, config: dict):
        self.db = enc_server.utils.DB(config)

    def test_init(self):
        self.setup_db({"mongoURI": DbTestSuite.mongo_uri})
        self.assertIsNotNone(self.db)

    def test_missing_init(self):
        self.assertRaises(KeyError, self.setup_db, {})

    def test_db(self):
        self.setup_db({"mongoURI": DbTestSuite.mongo_uri})
        self.assertIsNone(self.db.store_record(DbTestSuite.record_id, DbTestSuite.record_payload))
        self.assertEqual(DbTestSuite.record_payload, self.db.retrieve_record(DbTestSuite.record_id))
        self.assertIsNone(self.db.delete_record(DbTestSuite.record_id))

    def test_bad_store(self):
        self.setup_db({"mongoURI": DbTestSuite.bad_mongo_uri})
        self.assertRaises(RuntimeError, self.db.store_record, record_id=DbTestSuite.record_id,
                          record_payload=DbTestSuite.record_payload)

    def test_bad_retrieve(self):
        self.setup_db({"mongoURI": DbTestSuite.bad_mongo_uri})
        self.assertRaises(RuntimeError, self.db.retrieve_record, record_id=DbTestSuite.record_id)

    def test_bad_delete(self):
        self.setup_db({"mongoURI": DbTestSuite.bad_mongo_uri})
        self.assertRaises(RuntimeError, self.db.delete_record, record_id=DbTestSuite.record_id)


if __name__ == '__main__':
    unittest.main()
