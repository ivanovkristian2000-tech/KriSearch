from tabulate import tabulate


def format_search_params(search_type, params):
    if search_type == "keyword":
        return f"title keyword: {params['keyword']}"

    if search_type == "genre_years_range":
        return (
            f"genre_id: {params['genre_id']}, "
            f"years: {params['year_from']}-{params['year_to']}"
        )

    return str(params)


def print_top_searches(searches):
    print("\nTop 5 popular searches:")

    if not searches:
        print("No search history yet.")
        return

    table = []

    for i, search in enumerate(searches, start=1):
        search_type = search["_id"]["search_type"]
        params = search["_id"]["params"]
        params_text = format_search_params(search_type, params)

        table.append([
            i,
            search_type,
            params_text,
            search["count"],
            search["last_results_count"]
        ])

    print(tabulate(
        table,
        headers=["#", "Search type", "Params", "Count", "Results"],
        tablefmt="grid"
    ))


def print_latest_unique_searches(searches):
    print("\nLatest 5 unique searches:")

    if not searches:
        print("No search history yet.")
        return

    table = []

    for i, search in enumerate(searches, start=1):
        search_type = search["_id"]["search_type"]
        params = search["_id"]["params"]
        params_text = format_search_params(search_type, params)

        table.append([
            i,
            search_type,
            params_text,
            search["last_results_count"],
            search["last_timestamp"]
        ])

    print(tabulate(
        table,
        headers=["#", "Search type", "Params", "Results", "Last timestamp"],
        tablefmt="grid"
    ))


def print_title_movies(movies, start_number=1):
    if not movies:
        print("\nФильмы не найдены.")
        return

    table = []

    for i, movie in enumerate(movies, start=start_number):
        table.append([
            i,
            movie[0],
            movie[1]
        ])

    print(tabulate(
        table,
        headers=["#", "Title", "Year"],
        tablefmt="grid"
    ))


def print_genre_year_movies(movies, start_number=1):
    if not movies:
        print("\nФильмы не найдены.")
        return

    table = []

    for i, movie in enumerate(movies, start=start_number):
        table.append([
            i,
            movie[0],
            movie[1],
            movie[2]
        ])

    print(tabulate(
        table,
        headers=["#", "Title", "Year", "Genre"],
        tablefmt="grid"
    ))


def print_genres(genres):
    table = []

    for genre_id, genre_name in genres:
        table.append([genre_id, genre_name])

    print("\nСписок жанров:")
    print(tabulate(
        table,
        headers=["#", "Genre"],
        tablefmt="grid"
    ))


def print_year_range(year_range):
    print("\nДиапазон годов:")
    print(f"{year_range[0]}-{year_range[1]}")
