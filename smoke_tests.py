from local_settings import dbconfig
from mysql_connector import MovieDB
from mongo_logger import MongoLogger
from log_stats import MongoStats



def smoke_test_mysql():
    print("Running MySQL smoke test...")

    with MovieDB(dbconfig) as db:
        genres = db.get_genres()
        assert genres, "Genres list is empty"

        year_range = db.get_year_range()
        assert year_range[0] <= year_range[1], "Invalid year range"

        title_count = db.count_by_title("AIR")
        assert isinstance(title_count, int), "Title count must be integer"

        title_results = db.search_by_title("AIR")
        assert isinstance(title_results, list), "Title search result must be list"
        assert len(title_results) <= 10, "Title search should return max 10 rows"

        genre_count = db.count_by_category_and_years(1, 2000, 2012)
        assert isinstance(genre_count, int), "Genre/year count must be integer"

        genre_results = db.search_by_category_and_years(1, 2000, 2012)
        assert isinstance(genre_results, list), "Genre/year search result must be list"
        assert len(genre_results) <= 10, "Genre/year search should return max 10 rows"

    print("MySQL smoke test passed.")


def smoke_test_mongo():
    print("Running MongoDB smoke test...")

    with MongoLogger() as logger:
        logger.log_search(
            search_type="test",
            params={"source": "smoke_tests"},
            results_count=0
        )

    with MongoStats() as stats:
        top_searches = stats.get_top_searches()
        latest_unique = stats.get_latest_unique_searches()

        assert isinstance(top_searches, list), "Top searches must be list"
        assert isinstance(latest_unique, list), "Latest unique searches must be list"

    print("MongoDB smoke test passed.")


def run_smoke_tests():
    smoke_test_mysql()
    smoke_test_mongo()
    print("\nAll smoke tests passed.")


if __name__ == "__main__":
    run_smoke_tests()