import mysql.connector
from pydantic import BaseModel
from typing import List, Optional
import threading

db_lock = threading.Lock()

class Modulo(BaseModel):
    id: Optional[int] = None
    nombre: str
    duracion: int
    nivel: str

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    descripcion: str
    precio: float
    duracion: int

db_connection = mysql.connector.connect(
    host="devops0001.mysql.database.azure.com",
    user="devops",
    password="#braian987",
    database="devops"
)
db_cursor = db_connection.cursor()

def create_modulo_table():
    with db_lock:
        db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS modulos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                duracion INT,
                nivel VARCHAR(255)
            )
        ''')
        db_connection.commit()

def insert_modulo(modulo: Modulo):
    with db_lock:
        query = "INSERT INTO modulos (nombre, duracion, nivel) VALUES (%s, %s, %s)"
        values = (modulo.nombre, modulo.duracion, modulo.nivel)
        db_cursor.execute(query, values)
        db_connection.commit()

def get_all_modulos() -> List[Modulo]:
    with db_lock:
        db_cursor.execute("SELECT id, nombre, duracion, nivel FROM modulos")
        modulos = []
        for row in db_cursor.fetchall():
            modulo = Modulo(id=row[0], nombre=row[1], duracion=row[2], nivel=row[3])
            modulos.append(modulo)
        return modulos

def create_curso_table():
    with db_lock:
        db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS cursos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titulo VARCHAR(255) NOT NULL,
                descripcion TEXT,
                precio FLOAT,
                duracion INT
            )
        ''')
        db_connection.commit()

def insert_curso(curso: Curso):
    with db_lock:
        query = "INSERT INTO cursos (titulo, descripcion, precio, duracion) VALUES (%s, %s, %s, %s)"
        values = (curso.titulo, curso.descripcion, curso.precio, curso.duracion)
        db_cursor.execute(query, values)
        db_connection.commit()

def get_all_cursos() -> List[Curso]:
    with db_lock:
        db_cursor.execute("SELECT id, titulo, descripcion, precio, duracion FROM cursos")
        cursos = []
        for row in db_cursor.fetchall():
            curso = Curso(id=row[0], titulo=row[1], descripcion=row[2], precio=row[3], duracion=row[4])
            cursos.append(curso)
        return cursos

# Otras funciones como update_modulo, delete_modulo, update_curso, delete_curso, etc., seguirían un patrón similar.
# Se han omitido aquí por brevedad, pero puedes implementarlas de manera análoga.

def close_connection():
    db_connection.close()
