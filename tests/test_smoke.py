import pytest

from local_settings import dbconfig
from mysql_connector import MovieDB
from mongo_logger import MongoLogger
from log_stats import MongoStats


@pytest.fixture
def mysql_db():
    with MovieDB(dbconfig) as db:
        yield db


@pytest.fixture
def mongo_logger():
    with MongoLogger() as logger:
        yield logger


@pytest.fixture
def mongo_stats():
    with MongoStats() as stats:
        yield stats


def test_mysql_connection_and_genres(mysql_db):
    genres = mysql_db.get_genres()
    assert genres, "Genres list is empty"


def test_mysql_title_search(mysql_db):
    title_count = mysql_db.count_by_title("AIR")
    title_results = mysql_db.search_by_title("AIR")

    assert isinstance(title_count, int)
    assert isinstance(title_results, list)
    assert len(title_results) <= 10


def test_mysql_genre_year_search(mysql_db):
    genre_count = mysql_db.count_by_category_and_years(1, 2000, 2012)
    genre_results = mysql_db.search_by_category_and_years(1, 2000, 2012)

    assert isinstance(genre_count, int)
    assert isinstance(genre_results, list)
    assert len(genre_results) <= 10


def test_mongo_logger_write(mongo_logger):
    inserted_id = mongo_logger.log_search(
        search_type="test",
        params={"source": "pytest_smoke"},
        results_count=0
    )

    assert inserted_id is not None


def test_mongo_stats_read(mongo_stats):
    top_searches = mongo_stats.get_top_searches()
    latest_unique = mongo_stats.get_latest_unique_searches()

    assert isinstance(top_searches, list)
    assert isinstance(latest_unique, list)