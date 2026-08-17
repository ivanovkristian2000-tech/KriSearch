from pymongo import MongoClient

from local_settings import MONGODB_URL_WRITE


COLLECTION_NAME = "final_project_060326_ptm_Kristian_Ivanov"


class MongoConnection:
    """Context manager for MongoDB connection."""

    def __init__(self, mongo_url=MONGODB_URL_WRITE, db_name="ich_edit"):
        self.mongo_url = mongo_url
        self.db_name = db_name
        self.client = None
        self.collection = None

    def __enter__(self):
        self.client = MongoClient(self.mongo_url)
        db = self.client[self.db_name]
        self.collection = db[COLLECTION_NAME]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()
