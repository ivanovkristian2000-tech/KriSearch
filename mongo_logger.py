from datetime import datetime, timezone
from pymongo import MongoClient
from local_settings import MONGODB_URL_WRITE



COLLECTION_NAME = "final_project_060326_ptm_Kristian_Ivanov"



class MongoLogger:
    """Logger for saving user search history to MongoDB."""

    def __init__(self, mongo_url, db_name="ich_edit"):
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

    def log_search(self, search_type, params, results_count):
        log_document = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "search_type": search_type,
            "params": params,
            "results_count": results_count
        }

        self.collection.insert_one(log_document)



if __name__ == "__main__":
    with MongoLogger(MONGODB_URL_WRITE) as logger:
        logger.log_search(
            search_type="test",
            params={"keyword": "AIR"},
            results_count=7
        )

    print("Test log saved.")