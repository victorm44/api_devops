import mysql.connector
from pydantic import BaseModel
from typing import List, Optional
import threading

db_lock = threading.Lock()


class Movie(BaseModel):
    id: Optional[int] = None
    title: str
    overview: str
    year: int
    rating: float
    category: str

class Genre(BaseModel):
    id: Optional[int] = None
    name: str
    description: str

db_connection = mysql.connector.connect(
    host="devops0001.mysql.database.azure.com",
    user="devops",
    password="#braian987",
    database="devops"
)
db_cursor = db_connection.cursor()

def create_movie_table():
    with db_lock:
        db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                overview TEXT,
                year INT,
                rating FLOAT,
                category VARCHAR(255)
            )
        ''')
        db_connection.commit()

def insert_movie(movie: Movie):
    with db_lock:
        query = "INSERT INTO movies (title, overview, year, rating, category) VALUES (%s, %s, %s, %s, %s)"
        values = (movie.title, movie.overview, movie.year, movie.rating, movie.category)
        db_cursor.execute(query, values)
        db_connection.commit()

def get_all_movies() -> List[Movie]:
    with db_lock:
        db_cursor.execute("SELECT id, title, overview, year, rating, category FROM movies")
        movies = []
        for row in db_cursor.fetchall():
            movie = Movie(id=row[0], title=row[1], overview=row[2], year=row[3], rating=row[4], category=row[5])
            movies.append(movie)
        return movies
    
def create_tables():
    with db_lock:
        db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS genres (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT
            )
        ''')
        db_connection.commit()

def insert_genre(genre: Genre):
    with db_lock:
        query = "INSERT INTO genres (name, description) VALUES (%s, %s)"
        values = (genre.name, genre.description)
        db_cursor.execute(query, values)
        db_connection.commit()

def get_all_genres() -> List[Genre]:
    with db_lock:
        db_cursor.execute("SELECT id, name, description FROM genres")
        genres = []
        for row in db_cursor.fetchall():
            genre = Genre(id=row[0], name=row[1], description=row[2])
            genres.append(genre)
        return genres
    
def update_genre(updated_genre: Genre) -> Optional[Genre]:
    with db_lock:
        query = """
            UPDATE genres
            SET name = %s, description = %s
            WHERE id = %s
        """
        values = (
            updated_genre.name,
            updated_genre.description,
            updated_genre.id,
        )

        db_cursor.execute(query, values)
        db_connection.commit()

        return updated_genre

    
def update_movie(updated_movie: Movie) -> Optional[Movie]:
    with db_lock:
        query = """
            UPDATE movies
            SET title = %s, overview = %s, year = %s, rating = %s, category = %s
            WHERE id = %s
        """
        values = (
            updated_movie.title,
            updated_movie.overview,
            updated_movie.year,
            updated_movie.rating,
            updated_movie.category,
            updated_movie.id,
        )

        db_cursor.execute(query, values)
        db_connection.commit()

        return updated_movie


def delete_movie(movie_id: int) -> Optional[Movie]:
    with db_lock:
        query = "DELETE FROM movies WHERE id = %s"
        db_cursor.execute(query, (movie_id,))
        db_connection.commit()

        # Comprueba si algún registro fue eliminado
        if db_cursor.rowcount > 0:
            # Devuelve None en lugar de crear una instancia de Movie
            return None
        else:
            return None  # La película no fue encontrada

    
# En database.py
def delete_genre(genre_id: int) -> Optional[Genre]:
    with db_lock:
        query = "DELETE FROM genres WHERE id = %s"
        db_cursor.execute(query, (genre_id,))
        db_connection.commit()

        # Comprueba si algún registro fue eliminado
        if db_cursor.rowcount > 0:
            # Devuelve None en lugar de crear una instancia de Genre
            return None
        else:
            return None  # El género no fue encontrado



    
def drop_table(table_name: str):
    with db_lock:
        db_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        db_connection.commit()

#drop_table("genres")


def close_connection():
    db_connection.close()
