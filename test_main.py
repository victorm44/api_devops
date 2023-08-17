from fastapi.testclient import TestClient
from main import app
from database import close_connection, create_tables

# Inicializar el cliente de prueba
client = TestClient(app)

def setup_module(module):
    create_tables()

def teardown_module(module):
    close_connection()


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '<h1>Victor</h1>'

def test_read_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    assert len(response.json()) > 0  

def test_read_single_movie():
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Inception"

def test_read_movies_by_category():
    response = client.get("/movies/?category=Acción&year=2001")
    assert response.status_code == 200
    assert len(response.json()) >= 0 

# Pruebas de creación
def test_create_movie():
    new_movie = {
        "title": "New Movie",
        "overview": "New movie overview",
        "year": 2023,
        "rating": 8.0,
        "category": "Sci-Fi"
    }
    response = client.post("/movies", json=new_movie)
    assert response.status_code == 200
    assert response.json()["title"] == new_movie["title"]

