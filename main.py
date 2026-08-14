from mysql_connector import MovieDB
from mongo_logger import MongoLogger
from local_settings import dbconfig, MONGODB_URL_WRITE



def main_menu(db, logger):

    while True:

        print("\nKriSearch")
        print("\n1. Поиск по названию")
        print("2. Поиск по жанру и годам")
        print("3. Статистика")
        print("4. Выход\n")

        user_input = input("Введите номер: ")

        if user_input == "1":
            search_by_title_menu(db, logger)
        elif user_input == "2":
            search_by_genre_and_years_menu(db, logger)
        elif user_input == "3":
            print("menu 3")
        elif user_input == "4":
            break
        else:
            print("\nНе корректный ввод")



def search_by_title_menu(db, logger):
    while True:

        print("\n1. Ввести название фильма")
        print("2. Назад.\n")
        user_input = input("Введите номер: ")

        if user_input == "1":
            keyword = input("\nВведите название фильма: ").strip()

            if not keyword:
                print("\nВведите ключевое слово.")
                continue

            total_results = db.count_by_title(keyword)

            if total_results == 0:
                print("\nФильмы не найдены.")
                continue

            print(f"\nНайдено фильмов: {total_results}")

            logger.log_search(search_type="keyword", params={"keyword": keyword}, results_count=total_results)

            page_size = 10
            offset = 0

            while True:
                result = db.search_by_title(keyword, limit=page_size, offset=offset)

                for i, movie in enumerate(result, start=offset + 1):
                    print(f"{i}. {movie[0]} — {movie[1]}")

                if offset + page_size >= total_results:
                    print("\nБольше результатов нет.")
                    break

                while True:
                    next_page = input("\nПоказать следующие 10? y/n: ").lower().strip()

                    if next_page in ("y", "n"):
                        break

                    print("\nНекорректный ввод.")

                if next_page == "y":
                    offset += page_size
                else:
                    break

        elif user_input == "2":
            return
        else:
            print("\nНе корректный ввод")



def search_by_genre_and_years_menu(db, logger):

    print("Список жанров: ")
    genres = db.get_genres()

    for i, genre in genres:
        print(f"{i}. {genre}")

    print("\nДиапазон годов: ")
    year_range = db.get_year_range()

    print(f"{year_range[0]}-{year_range[1]} ")

    while True:
        user_genre = input("Введите номер жанра: ").strip()

        if not user_genre:
            continue

        if not user_genre.isdigit():
            print("Номер жанра должен быть числом.")
            continue

        genre_num = int(user_genre)

        if genre_num < 1 or genre_num > len(genres):
            print("Такого жанра нет.")
            continue

        while True:
            user_year_from = input("Год с: ").strip()
            user_year_to = input("Год до: ").strip()

            if not user_year_from or not user_year_to:
                print("Введите оба года.")
                continue

            if not user_year_from.isdigit() or not user_year_to.isdigit():
                print("Годы должны быть числами.")
                continue

            year_from = int(user_year_from)
            year_to = int(user_year_to)

            if not year_range[0] <= year_from <= year_range[1]:
                print(f"\nГод с должен быть в диапазоне {year_range[0]}-{year_range[1]}.")
                continue

            if not year_range[0] <= year_to <= year_range[1]:
                print(f"\nГод до должен быть в диапазоне {year_range[0]}-{year_range[1]}.")
                continue

            if year_from > year_to:
                print("Год с не может быть больше года до.")
                continue

            break

        break

    total_results = db.count_by_category_and_years(genre_num, year_from, year_to)
    logger.log_search(
        search_type="genre_years_range",
        params={
            "genre_id": genre_num,
            "year_from": year_from,
            "year_to": year_to},
        results_count=total_results
    )

    if total_results == 0:
        print("\nФильмы не найдены.")
        return

    print(f"\nНайдено фильмов: {total_results}")

    page_size = 10
    offset = 0

    while True:
        result = db.search_by_category_and_years(
            genre_num,
            year_from,
            year_to,
            limit=page_size,
            offset=offset
        )
        for i, movie in enumerate(result, start=offset + 1):
            print(f"{i}. {movie[0]} — {movie[1]} — {movie[2]}")

        if offset + page_size >= total_results:
            print("\nРезультатов больше нет.")
            break

        user_input_y_n = input("\nПоказать следующие 10 фильмов? y/n: ").lower().strip()

        if user_input_y_n == "y":
            offset += page_size
        elif user_input_y_n == "n":
            break
        else:
            print("\nНекорректный ввод.")
            break
















if __name__ == "__main__":
    with MovieDB(dbconfig) as db, MongoLogger(MONGODB_URL_WRITE) as logger:
        main_menu(db, logger)



