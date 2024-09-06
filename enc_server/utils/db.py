import abc
import config
import pymongo


class DBInterface(abc.ABC):
    @abc.abstractmethod
    def store_record(self, record_id: str, record_payload: str):
        pass

    @abc.abstractmethod
    def retrieve_record(self, record_id: str) -> str:
        pass

    @abc.abstractmethod
    def delete_record(self, record_id: str):
        pass


class DB(DBInterface):
    db_name = "enc-server-go"
    db_collection = "records"

    def __init__(self, configs):
        result, missing = config.verify_configs(configs, ["mongoURI"])
        if not result:
            raise KeyError("ConnSocket missing configuration" + missing)

        self.mongo_uri = configs["mongoURI"]

    def store_record(self, record_id: str, record_payload: str):
        collection = self.__get_record_collection()
        id_filter = {"_id": record_id}
        entry = {"$set": {"_id": record_id, "record": record_payload}}
        collection.update_one(id_filter, entry, upsert=True)

    def retrieve_record(self, record_id: str) -> str:
        collection = self.__get_record_collection()
        entry = collection.find_one({"_id": record_id})
        record_payload = entry["record"]
        return record_payload

    def delete_record(self, record_id: str):
        collection = self.__get_record_collection()
        collection.delete_one({"_id": record_id})

    def __get_record_collection(self):
        client = pymongo.MongoClient(self.mongo_uri)
        db = client[DB.db_name]
        collection = db[DB.db_collection]
        return collection
