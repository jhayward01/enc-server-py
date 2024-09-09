import config
import pymongo
from pymongo.collection import Collection, Mapping, Any


class DB:
    db_name = "enc-server-go"
    db_collection = "records"

    def __init__(self, configs: dict):
        result, missing = config.verify_configs(configs, ["mongoURI"])
        if not result:
            raise KeyError("DB missing configuration " + missing)

        self.mongo_uri = configs["mongoURI"]

    def store_record(self, record_id: str, record_payload: str):
        try:
            collection = self.__get_record_collection()
            id_filter = {"_id": record_id}
            entry = {"$set": {"_id": record_id, "record": record_payload}}
            collection.update_one(id_filter, entry, upsert=True)
        except Exception as err:
            raise RuntimeError(err) from None

    def retrieve_record(self, record_id: str) -> str:
        try:
            collection = self.__get_record_collection()
            entry = collection.find_one({"_id": record_id})
            record_payload = entry["record"]
            return record_payload
        except Exception as err:
            raise RuntimeError(err) from None

    def delete_record(self, record_id: str):
        try:
            collection = self.__get_record_collection()
            collection.delete_one({"_id": record_id})
        except Exception as err:
            raise RuntimeError(err) from None

    def __get_record_collection(self) -> Collection[Mapping[str, Any]]:
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[DB.db_name]
        collection = db[DB.db_collection]
        return collection
