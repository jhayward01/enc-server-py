import abc
import pymongo


def get_record_collection():
    print("Connecting to data store...")

    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    print(my_client.list_database_names())


class DBInterface(abc.ABC):
    @abc.abstractmethod
    def store_record(self, id: str, record: str):
        pass

    @abc.abstractmethod
    def retrieve_record(self, id: str) -> str:
        pass

    @abc.abstractmethod
    def delete_record(self, id: str):
        pass


class DB(DBInterface):

    def __init__(self, server_addr):
        self.server_host = server_addr.split(":")[0]
        self.server_port = int(server_addr.split(":")[1])
