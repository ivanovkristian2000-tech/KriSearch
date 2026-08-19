from datetime import datetime, timezone
from mongo_connection import MongoConnection


class MongoLogger(MongoConnection):
    """Logger for saving user search history to MongoDB."""

    def log_search(self, search_type, params, results_count):
        log_document = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "search_type": search_type,
            "params": params,
            "results_count": results_count
        }

        result = self.collection.insert_one(log_document)
        return result.inserted_id
