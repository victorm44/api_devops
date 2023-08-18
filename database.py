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
    host="localhost",
    user="root",
    password="my-secret-pw",
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
    
def update_movie(updated_movie: Movie) -> Optional[Movie]:
    try:
        with db_lock:
            db_connection = mysql.connector.connect(
                host="your_db_host",
                user="your_db_user",
                password="your_db_password",
                database="your_db_name"
            )
            
            db_cursor = db_connection.cursor()

            db_cursor.execute('''
                UPDATE movies
                SET title=%s, overview=%s, year=%s, rating=%s, category=%s
                WHERE id=%s
            ''', (
                updated_movie.title,
                updated_movie.overview,
                updated_movie.year,
                updated_movie.rating,
                updated_movie.category,
                updated_movie.id
            ))

            db_connection.commit()
            db_cursor.close()
            db_connection.close()

            return updated_movie
    except Exception as e:
        print("Error updating movie:", e)
        return None
    
def drop_table(table_name: str):
    with db_lock:
        db_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        db_connection.commit()

#drop_table("genres")


def close_connection():
    db_connection.close()
