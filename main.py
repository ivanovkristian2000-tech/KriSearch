from mysql_connector import MovieDB
from local_settings import dbconfig


class InputUserError(Exception):
    """ Raised when user input is invalid. """


# for i, genre in enumerate(genres, start=1):
#     print(f"{i}. {genre[0]}")



def main_menu(db):

    while True:

        print("\nKriSearch")
        print("\n1. Поиск по названию")
        print("2. Поиск по жанру и годам")
        print("3. Статистика")
        print("4. Выход\n")

        user_input = input("Введите номер: ")

        if user_input == "1":
            search_by_title_menu(db)
        elif user_input == "2":
            print("menu 2")
        elif user_input == "3":
            print("menu 3")
        elif user_input == "4":
            break
        else:
            print("\nНе корректный ввод")



def search_by_title_menu(db):
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






















if __name__ == "__main__":
    with MovieDB(dbconfig) as db:
        main_menu(db)



