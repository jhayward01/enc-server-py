import unittest

import enc_server


class BEServerTestSuite(unittest.TestCase):
    configs = {'port': '8888', 'mongoURI': 'mongodb://localhost:27017/?timeoutMS=200'}
    bad_configs = {'port': '8888', 'mongoURI': 'mongodb://foo:27017/?timeoutMS=200'}

    record_id_enc = "396263343233393039616335acc30dd405c51d37675d4e0002a526ae113d56"

    record_payload_enc = ("396263343233393039616335b6d61c6839a0dda2524d19b4e5d" +
                          "ac5a1fda8902ad2701ced5c31c89088c3151d039ee27d003b75c3a140141c05da496572142eb" +
                          "5466c5edb07de33d8ac301f19789fbef68e5c3f280bf4f274e8d2d2d7")

    def test_init(self):
        self.assertIsNotNone(enc_server.be.server.Server(BEServerTestSuite.configs))

    def test_bad_init(self):
        self.assertRaises(KeyError, enc_server.be.server.Server, {})

    def test_empty_msg(self):
        server = enc_server.be.server.Server(BEServerTestSuite.configs)

        empty_message = f"\n".encode('utf-8')
        empty_response = server.respond(empty_message)
        self.assertTrue(empty_response.decode('utf-8').startswith("ERROR Malformed"))

    def test_unknown_msg(self):
        server = enc_server.be.server.Server(BEServerTestSuite.configs)

        unknown_message = f"FOO\n".encode('utf-8')
        unknown_response = server.respond(unknown_message)
        self.assertTrue(unknown_response.decode('utf-8').startswith("ERROR Malformed"))

    def test_bad_store(self):
        server = enc_server.be.server.Server(BEServerTestSuite.bad_configs)

        store_message = f"STORE {BEServerTestSuite.record_id_enc} {BEServerTestSuite.record_payload_enc}\n".encode(
            'utf-8')
        store_response = server.respond(store_message)
        self.assertTrue(store_response.decode('utf-8').startswith("ERROR"))

    def test_malformed_store(self):
        server = enc_server.be.server.Server(BEServerTestSuite.configs)

        store_message = f"STORE\n".encode('utf-8')
        store_response = server.respond(store_message)
        self.assertTrue(store_response.decode('utf-8').startswith("ERROR Malformed"))

    def test_bad_retrieve(self):
        server = enc_server.be.server.Server(BEServerTestSuite.bad_configs)

        retrieve_message = f"RETRIEVE {BEServerTestSuite.record_id_enc}\n".encode('utf-8')
        retrieve_response = server.respond(retrieve_message)
        self.assertTrue(retrieve_response.decode('utf-8').startswith("ERROR"))

    def test_malformed_retrieve(self):
        server = enc_server.be.server.Server(BEServerTestSuite.configs)

        retrieve_message = f"RETRIEVE\n".encode('utf-8')
        retrieve_response = server.respond(retrieve_message)
        self.assertTrue(retrieve_response.decode('utf-8').startswith("ERROR Malformed"))

    def test_bad_delete(self):
        server = enc_server.be.server.Server(BEServerTestSuite.bad_configs)

        delete_message = f"DELETE {BEServerTestSuite.record_id_enc}\n".encode('utf-8')
        delete_response = server.respond(delete_message)
        self.assertTrue(delete_response.decode('utf-8').startswith("ERROR"))

    def test_malformed_delete(self):
        server = enc_server.be.server.Server(BEServerTestSuite.configs)

        delete_message = f"DELETE\n".encode('utf-8')
        delete_response = server.respond(delete_message)
        self.assertTrue(delete_response.decode('utf-8').startswith("ERROR Malformed"))

    def test_db(self):
        server = enc_server.be.server.Server(BEServerTestSuite.configs)

        store_message = f"STORE {BEServerTestSuite.record_id_enc} {BEServerTestSuite.record_payload_enc}\n".encode(
            'utf-8')
        store_response = server.respond(store_message)
        self.assertEqual("SUCCESS", store_response.decode('utf-8').strip())

        retrieve_message = f"RETRIEVE {BEServerTestSuite.record_id_enc}\n".encode('utf-8')
        retrieve_response = server.respond(retrieve_message)
        self.assertEqual(BEServerTestSuite.record_payload_enc, retrieve_response.decode('utf-8').strip())

        delete_message = f"DELETE {BEServerTestSuite.record_id_enc}\n".encode('utf-8')
        delete_response = server.respond(delete_message)
        self.assertEqual("", delete_response.decode('utf-8').strip())
