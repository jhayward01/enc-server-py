from enc_server import utils, be


class Server(utils.Responder):
    expected_fields = {"STORE": 3, "RETRIEVE": 2, "DELETE": 2}

    def __init__(self, configs: dict):
        self.keygen = utils.Keygen(configs)
        self.be_client = be.client.Client(configs)

    def respond(self, msg: bytes) -> bytes:
        s = msg.decode('utf-8').strip()
        fields = s.split()

        if (not fields or fields[0] not in Server.expected_fields or
                len(fields) != Server.expected_fields[fields[0]]):
            return f"ERROR Malformed request: {s}\n".encode('utf-8')

        if fields[0] == "STORE":
            try:
                key, nonce = self.keygen.random_key(), self.keygen.random_nonce()
                cipher = utils.Cipher({"key": key, "nonce": nonce})
                id_enc = cipher.encrypt(fields[1].encode('utf-8')).decode('utf-8')
                record_enc = cipher.encrypt(fields[2].encode('utf-8')).decode('utf-8')
                self.be_client.store(id_enc, record_enc)
            except RuntimeError as err:
                return f"ERROR: {err}\n".encode('utf-8')
            else:
                return key

            # func (s *serverImpl) storeRecord(id, record []byte) (key []byte, err error) {
            #
            # 	// Generate cipher entry for ID.
            # 	idEncrypt := s.idCipher.Seal(s.idNonce, s.idNonce, id, nil)
            #
            # 	// Generate random AES key.
            # 	if key, err = s.keygen.RandomKey(); err != nil {
            # 		return nil, err
            # 	}
            #
            # 	// Generate key, cipher, and nonce for record.
            # 	cipher, err := s.keygen.GetGCMCipher(key)
            # 	if err != nil {
            # 		return nil, err
            # 	}
            #
            # 	// Randomly generate nonce (initialization vector).
            # 	nonce, err := s.keygen.RandomNonce(cipher.NonceSize())
            # 	if err != nil {
            # 		return nil, err
            # 	}
            #
            # 	// Generate cipher entry for record. Place in data store.
            # 	recordEncrypt := cipher.Seal(nonce, nonce, record, nil)
            # 	if err = s.beClient.StoreRecord(idEncrypt, recordEncrypt); err != nil {
            # 		return nil, err
            # 	}
            #
            # 	return key, nil
            # }