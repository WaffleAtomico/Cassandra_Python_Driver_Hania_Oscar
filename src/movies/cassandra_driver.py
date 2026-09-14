import uuid

from cassandra.cluster import Cluster

# ==============================
# CQL Statements
# ==============================


CREATE_KEYSPACE = "CREATE KEYSPACE IF NOT EXISTS movies WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
CREATE_TABLE_MOVIE_BY_TITLE = """CREATE TABLE IF NOT EXISTS movies.movie_by_title
                                                    (movie_id uuid,
                                                    title text,
                                                    release_year int,
                                                    director text,
                                                    genre text,
                                                    rating float,
                                                    PRIMARY KEY (title, release_year)
                                                    );"""
CREATE_TABLE_MOVIE_BY_GENRE = """CREATE TABLE IF NOT EXISTS movies.movie_by_genre
                                                    (movie_id uuid,
                                                    title text,
                                                    release_year int,
                                                    director text,
                                                    genre text,
                                                    rating float,
                                                    PRIMARY KEY ((title, genre), rating)
                                                    );"""
INSERT_MOVIE_TITLE = "INSERT INTO movies.movie_by_title (movie_id, title, release_year, director, genre, rating) VALUES (?, ?, ?, ?, ?, ?);"
INSERT_MOVIE_GENRE = "INSERT INTO movies.movie_by_genre (movie_id, title, release_year, director, genre, rating) VALUES (?, ?, ?, ?, ?, ?);"
DELETE_MOVIE_TITLE = "DELETE FROM movies.movie_by_title WHERE title=? AND release_year=?"
DELETE_MOVIE_GENRE = "DELETE FROM movies.movie_by_genre WHERE genre=? AND title=?"
UPDATE_DIRECTOR_IN_TITLE = "UPDATE movies.movie_by_title SET director=? WHERE title=? AND release_year=?"
UPDATE_DIRECTOR_IN_GENRE = "UPDATE movies.movie_by_genre SET director=? WHERE genre=? AND title=?"
SELECT_BY_TITLE = "SELECT * FROM movies.movie_by_title WHERE title=? AND release_year=?"
SELECT_BY_GENRE = "SELECT * FROM movies.movie_by_genre WHERE genre=?"


# ==============================
# Funciones base
# ==============================

def create_keyspace_and_tables(session):
    session.prepare(CREATE_KEYSPACE)
    session.execute(CREATE_KEYSPACE)

    # Create tables

    stmt = session.prepare(CREATE_TABLE_MOVIE_BY_TITLE)
    session.execute(stmt)

    stmt = None
    stmt = session.prepare(CREATE_TABLE_MOVIE_BY_GENRE)
    session.execute(stmt)

def insert_movie(session, title, year, director, genre, rating):
    new_movie_id = uuid.uuid4()
    stmt = session.prepare(INSERT_MOVIE_TITLE)
    session.execute(stmt, (new_movie_id, title, year, director, genre, rating))

    stmt = None
    stmt = session.prepare(INSERT_MOVIE_GENRE)
    session.execute(stmt, (new_movie_id, title, year, director, genre, rating))

def query_by_title(session, title, year):
    stmt = session.prepare(SELECT_BY_TITLE)
    rows = session.execute(stmt, (title, year))
    return rows

def query_by_genre(session, genre):
    stmt = session.prepare(SELECT_BY_GENRE)
    rows = session.execute(stmt, (genre))
    return rows

def update_movie_director(session, title, genre, year, new_director):
    stmt = session.prepare(UPDATE_DIRECTOR_IN_TITLE)
    session.execute(stmt, (new_director, title, year))

    stmt = None  # Hacemos esto para evitar problemas de referencias

    stmt = session.prepare(UPDATE_DIRECTOR_IN_GENRE)
    session.execute(stmt, (new_director, genre, title))

def delete_movie(session, title, genre, release_year):
    stmt = session.prepare(DELETE_MOVIE_TITLE)
    session.execute(stmt, (title, release_year))

    stmt = None

    stmt = session.prepare(DELETE_MOVIE_GENRE)
    session.execute(stmt, (genre, title))

# ==============================
# Menú
# ==============================

def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    create_keyspace_and_tables(session)

    id_width = 36
    title_width = 30
    year_width = 6
    director_width = 20
    genre_width = 15
    rating_width = 6
    
    while True:
        print("\n=== Movie Database Menu ===")
        print("1. Insertar película")
        print("2. Consultar por título")
        print("3. Consultar por género")
        print("4. Actualizar director")
        print("0. Salir")
        choice = input("Seleccione opción: ")
        if choice == "1":
            title = input("Título: ")
            year = int(input("Año: "))
            director = input("Director: ")
            genre = input("Género: ")
            rating = float(input("Rating: "))
            insert_movie(session, title=title, year=year, director=director, genre=genre, rating=rating)
        elif choice == "2":
            title = input("Título: ")
            year = int(input("Año: "))
            data = query_by_title(session, title, year)
            if data:
                print(
                        f"{'ID':<{id_width}}|{'Título':<{title_width}}|{'Año':<{year_width}}|{'Director':<{director_width}}|{'Género':<{genre_width}}|{'Rating':<{rating_width}}|"
                    )
                print("-" * (id_width + title_width + year_width + director_width + genre_width + rating_width + 6))

                for row in data:
                    print(
                        f"{str(row.movie_id):<{id_width}}|{str(row.title):<{title_width}}|{str(row.release_year):<{year_width}}|{str(row.director):<{director_width}}|{str(row.genre):<{genre_width}}|{row.rating:<{rating_width}.1f}|"
                    )
            else:
                print("No se encontraron resultados.")
        elif choice == "3":
            genre = input("Género: ")
            data = query_by_genre(session, genre)
            if data:

                print(
                    f"{'ID':<{id_width}}|{'Título':<{title_width}}|{'Año':<{year_width}}|{'Director':<{director_width}}|{'Género':<{genre_width}}|{'Rating':<{rating_width}}|"
                )
                print("-" * (id_width + title_width + year_width + director_width + genre_width + rating_width + 6))
                for row in data:
                    print(
                        f"{str(row.movie_id):<{id_width}}|{str(row.title):<{title_width}}|{str(row.release_year):<{year_width}}|{str(row.director):<{director_width}}|{str(row.genre):<{genre_width}}|{row.rating:<{rating_width}.1f}|"
                    )
            else:
                print("No se encontraron resultados.")
        elif choice == "4":
            title = input("Título: ")
            genre = input("Género: ")
            year = int(input("Año: "))
            new_director = input("Nuevo Director: ")
            update_movie_director(session, title, genre, year, new_director)
        elif choice == "5":
            # Eliminar de movie_by_title -> title, release_year
            # Eliminar de movie_by_genre -> genre, rating
            title = input("Título: ")
            genre = input("Género: ")
            rating = input("Rating: ")
            release_year = input("Año: ")
            delete_movie(session, title, genre, release_year)
        elif choice == '0':
            session.shutdown()
            break
        else:
            print("Opción inválida")
            break

if __name__ == "__main__":
    main()