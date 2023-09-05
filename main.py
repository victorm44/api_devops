from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from typing import List
from pydantic import BaseModel
from database import Genre, Movie, create_tables, insert_genre, get_all_genres, close_connection, \
    create_movie_table, insert_movie, get_all_movies, update_movie, close_connection
from fastapi import FastAPI

app = FastAPI()



app = FastAPI()
create_tables()
create_movie_table()
app.title = "Movies API"
app.version = "0.0.1"

@app.get('/genres', response_model=List[Genre], tags=['Genres'])
def get_genres():
    genres = get_all_genres()
    return genres

@app.post('/genres', response_model=Genre, tags=['Genres'])
def create_genre(genre: Genre):
    insert_genre(genre)
    return genre

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Victor</h1>')

@app.get('/movies', response_model=List[Movie], tags=['Movies'])
def get_movies():
    movies = get_all_movies()
    return movies

@app.get('/movies/{id}', response_model=Movie, tags=['Movies'])
def get_movie(id: int):
    movies = get_all_movies()
    for movie in movies:
        if movie.id == id:
            return movie
    return None

@app.get('/movies/', response_model=List[Movie], tags=['Movies'])
def get_movies_by_category(category: str, year: int):
    movies = get_all_movies()
    return [item for item in movies if item.category == category]

@app.post('/movies', response_model=Movie, tags=['Movies'])
def create_movie(movie: Movie):
    new_id = max(movie.id for movie in get_all_movies()) + 1 if get_all_movies() else 1
    movie.id = new_id
    insert_movie(movie)
    return movie

@app.put('/movies/{id}', response_model=Movie, tags=['Movies'])
def update_movie_endpoint(id: int, movie: Movie):
    existing_movie = None
    movies = get_all_movies()

    for m in movies:
        if m.id == id:
            existing_movie = m
            break

    if existing_movie is None:
        return {"message": "Movie not found"}

    updated_movie = movie.copy(update={'id': existing_movie.id})
    updated = update_movie(updated_movie)

    if updated:
        return updated
    return {"message": "Update failed"}

@app.delete('/movies/{id}', response_model=Movie, tags=['Movies'])
def delete_movie(id: int):
    movies = get_all_movies()
    for movie in movies:
        if movie.id == id:
            deleted_movie = movie
            return deleted_movie
    return {"message": "Movie not found"}

@app.on_event("shutdown")
def shutdown_event():
    close_connection()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)