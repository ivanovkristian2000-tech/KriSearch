import mysql.connector
from local_settings import dbconfig


class MySQLConnector:
    """ Context manager for MySQL connection """

    def __init__(self, db_config, autocommit=False):
        self.db_config = db_config
        self.autocommit = autocommit
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """ Create connection to DB cursor and autocommit """

        self.connection = mysql.connector.connect(**self.db_config)
        self.cursor = self.connection.cursor()
        self.connection.autocommit = self.autocommit
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Commit or rollback transaction and close connection. """
        try:
            if not self.autocommit:
                if exc_type is None:
                    self.connection.commit()
                else:
                    self.connection.rollback()

        except mysql.connector.Error as e:
            print("Commit Error", e)

        finally:
            if self.cursor:
                self.cursor.close()

            if self.connection:
                self.connection.close()


class MovieDB(MySQLConnector):
    """ Execute SQL queries for movie search """

    def get_genres(self):
        self.cursor.execute("SELECT category_id, name FROM category ORDER BY category_id")
        genres = self.cursor.fetchall()
        return genres

    def get_year_range(self):
        self.cursor.execute(
            """
            SELECT 
                min(release_year) AS min_year,
                max(release_year) AS max_year
            FROM
                film       
            """)

        years = self.cursor.fetchone()
        return years

    def search_by_title(self, keyword, limit=10, offset=0):
        pattern = f"%{keyword}%"
        self.cursor.execute("""
        SELECT 
            title,
            release_year 
        FROM
            film
        WHERE
            title LIKE %s
        LIMIT %s
        OFFSET %s
        """, (pattern, limit, offset))

        title = self.cursor.fetchall()
        return title

    def search_by_category_and_years(self, category, year_from, year_to, limit=10, offset=0):
        self.cursor.execute("""
        SELECT
            f.title AS movie_title,  
            f.release_year AS year,  
            c.name AS genre 
        FROM
            film AS f
                JOIN 
            film_category AS fc
            ON f.film_id = fc.film_id 
                JOIN
            category AS c
            ON fc.category_id = c.category_id
        WHERE
            c.category_id = %s
            AND f.release_year BETWEEN %s AND %s
        LIMIT %s 
        OFFSET %s
        """, (category, year_from, year_to, limit, offset))

        searching = self.cursor.fetchall()
        return searching

    def count_by_title(self, title):
        pattern = f"%{title}%"
        self.cursor.execute("""
        SELECT 
            COUNT(*) AS total_results
        FROM
            film
        WHERE
            title LIKE %s
        """, (pattern,))

        count_title = self.cursor.fetchone()
        return count_title[0]

    def count_by_category_and_years(self, category, year_from, year_to):
        self.cursor.execute("""
        SELECT
            COUNT(*) AS movies_found
        FROM
            film AS f
                JOIN 
            film_category AS fc
            ON f.film_id = fc.film_id 
                JOIN
            category AS c
            ON fc.category_id = c.category_id
        WHERE
            c.category_id = %s
            AND f.release_year BETWEEN %s AND %s
        """, (category, year_from, year_to))

        count_category = self.cursor.fetchone()
        return count_category[0]


if __name__ == "__main__":
    with MovieDB(dbconfig) as mv:
        print("Genres:")
        print(mv.get_genres())

        print("\nYear range:")
        print(mv.get_year_range())

        print("\nSearch by title:")
        print(mv.search_by_title("AIR", 10, 0))

        print("\nCount by title:")
        print(mv.count_by_title("AIR"))

        print("\nSearch by genre and years:")
        print(mv.search_by_category_and_years("1", 2000, 2012, 10, 0))

        print("\nCount by genre and years:")
        print(mv.count_by_category_and_years("Action", 2000, 2012))
