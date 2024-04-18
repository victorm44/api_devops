from flask.testing import FlaskClient
from app import app
from database import close_connection, create_curso_table, create_modulo_table

# Inicializar el cliente de prueba
client = app.test_client()

def setup_module(module):
    create_modulo_table()
    create_curso_table()

def teardown_module(module):
    close_connection()

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert b"Cursos API" in response.data

def test_get_modulos():
    response = client.get("/modulos")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_modulo():
    new_modulo = {
        "nombre": "Nuevo Módulo",
        "duracion": 120,
        "nivel": "Intermedio"
    }
    response = client.post("/modulos", json=new_modulo)
    assert response.status_code == 200
    assert response.json["nombre"] == new_modulo["nombre"]

def test_get_cursos():
    response = client.get("/cursos")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_curso():
    new_curso = {
        "titulo": "Nuevo Curso",
        "descripcion": "Descripción del nuevo curso",
        "precio": 99.99,
        "duracion": 240
    }
    response = client.post("/cursos", json=new_curso)
    assert response.status_code == 200
    assert response.json["titulo"] == new_curso["titulo"]