from mongo_connection import MongoConnection


class MongoStats(MongoConnection):
    """Read search statistics from MongoDB."""

    def get_top_searches(self, limit=5):
        pipeline = [
            {
                "$match": {
                    "search_type": {"$ne": "test"}
                }
            },
            {
                "$sort": {
                    "timestamp": -1
                }
            },
            {
                "$group": {
                    "_id": {
                        "search_type": "$search_type",
                        "params": "$params"
                    },
                    "count": {"$sum": 1},
                    "last_timestamp": {"$first": "$timestamp"},
                    "last_results_count": {"$first": "$results_count"}
                }
            },
            {
                "$sort": {
                    "count": -1
                }
            },
            {
                "$limit": limit
            }
        ]

        return list(self.collection.aggregate(pipeline))

    def get_latest_unique_searches(self, limit=5):
        pipeline = [
            {
                "$match": {
                    "search_type": {"$ne": "test"}
                }
            },
            {
                "$sort": {
                    "timestamp": -1
                }
            },
            {
                "$group": {
                    "_id": {
                        "search_type": "$search_type",
                        "params": "$params"
                    },
                    "last_timestamp": {"$first": "$timestamp"},
                    "last_results_count": {"$first": "$results_count"}
                }
            },
            {
                "$sort": {
                    "last_timestamp": -1
                }
            },
            {
                "$limit": limit
            }
        ]

        return list(self.collection.aggregate(pipeline))


if __name__ == "__main__":
    from formatter import print_top_searches, print_latest_unique_searches

    with MongoStats() as stats:
        top_searches = stats.get_top_searches()
        latest_unique = stats.get_latest_unique_searches()

    print_top_searches(top_searches)
    print_latest_unique_searches(latest_unique)
