import uuid

from cassandra.cluster import Cluster

# ==============================
# CQL Statements
# ==============================


CREATE_KEYSPACE = "CREATE KEYSPACE IF NOT EXISTS movies WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};"
CREATE_TABLE_MOVIE_BY_TITLE = """CREATE TABLE IF NOT EXISTS movies.movie_by_title"
                                                    (movie_id uuid,
                                                    title text, 
                                                    release_year int,
                                                    director text,
                                                    genre text,
                                                    rating float,
                                                    PRIMARY KEY (title, release_year)
                                                    );
                             """
CREATE_TABLE_MOVIE_BY_GENRE = """CREATE TABLE IF NOT EXISTS movies.movie_by_genre 
                                                    (movie_id uuid,
                                                    title text,
                                                    release_year int,
                                                    director text, 
                                                    genre text,
                                                    rating float, 
                                                    PRIMARY KEY ((title, genre), rating)
                                                    );
                              """
INSERT_MOVIE_TITLE = "INSERT INTO movies.movie_by_title (movie_id, title, release_year, director, genre, rating) VALUES (?, ?, ?, ?, ?, ?);"
INSERT_MOVIE_GENRE = "INSERT INTO movies.movie_by_genre (movie_id, title, release_year, director, genre, rating) VALUES (?, ?, ?, ?, ?, ?);"
DELETE_MOVIE_TITLE = "DELETE FROM movies.movie_by_title WHERE title=? AND release_year=?"
DELETE_MOVIE_GENRE = "DELETE FROM movies.movie_by_genre WHERE genre=? AND title=?"
SELECT_BY_TITLE = "SELECT * FROM movies.movie_by_title WHERE title=? AND release_year=?"
SELECT_BY_GENRE = "SELECT * FROM movies.movie_by_genre WHERE genre=?"


# ==============================
# Funciones base
# ==============================

def create_keyspace_and_tables(session: Cluster.Session):
    session.prepare(CREATE_KEYSPACE)
    session.execute(CREATE_KEYSPACE)

    # Create tables
    
    session.prepare(CREATE_TABLE_MOVIE_BY_TITLE)
    session.execute(CREATE_TABLE_MOVIE_BY_TITLE)

    session.prepare(CREATE_TABLE_MOVIE_BY_GENRE)
    session.execute(CREATE_TABLE_MOVIE_BY_GENRE)

def insert_movie(session, title, year, director, genre, rating):
    new_movie_id = uuid.uuid4()
    session.prepare(INSERT_MOVIE_TITLE)
    session.execute(INSERT_MOVIE_TITLE, (new_movie_id, title, year, director, genre, rating))

    session.prepare(INSERT_MOVIE_GENRE)
    session.execute(INSERT_MOVIE_GENRE, (new_movie_id, genre, title, year, director, rating))

    pass

def query_by_title(session, title, year):
    session.prepare(SELECT_BY_TITLE)
    session.execute(SELECT_BY_TITLE, (title, year))
    pass

def query_by_genre(session, genre):
    session.prepare(SELECT_BY_GENRE)
    session.execute(SELECT_BY_GENRE, (genre))
    pass

def update_movie_director(session, title, genre, new_director):

    pass

def delete_movie(session, title, genre, release_year):
    session.prepare(DELETE_MOVIE_TITLE)
    session.execute(DELETE_MOVIE_TITLE, (title, release_year))
    session.prepare(DELETE_MOVIE_GENRE)
    session.execute(DELETE_MOVIE_GENRE, (genre, title))
    pass

# ==============================
# Menú
# ==============================

def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    create_keyspace_and_tables(session)
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
            insert_movie(session, title, year, director, genre, rating)
        elif choice == "2":
            title = input("Título: ")
            year = int(input("Año: "))
            query_by_title(session, title, year)
        elif choice == "3":
            genre = input("Género: ")
            query_by_genre(session, genre)
        elif choice == "4":
            title = input("Título: ")
            genre = input("Género: ")
            new_director = input("Nuevo Director: ")
            update_movie_director(session, title, genre, new_director)
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