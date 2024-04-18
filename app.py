from flask import Flask, jsonify
from database import Modulo, Curso, create_modulo_table, create_curso_table, insert_modulo, insert_curso, \
    get_all_modulos, get_all_cursos, close_connection
from flask import request

app = Flask(__name__)
create_modulo_table()
create_curso_table()

@app.route('/modulos', methods=['GET'])
def get_modulos():
    modulos = get_all_modulos()
    return jsonify([modulo.dict() for modulo in modulos])

@app.route('/modulos', methods=['POST'])
def create_modulo():
    modulo_data = request.get_json()
    modulo = Modulo(**modulo_data)
    insert_modulo(modulo)
    return jsonify(modulo.dict())

@app.route('/cursos', methods=['GET'])
def get_cursos():
    cursos = get_all_cursos()
    return jsonify([curso.dict() for curso in cursos])

@app.route('/cursos', methods=['POST'])
def create_curso():
    curso_data = request.get_json()
    curso = Curso(**curso_data)
    insert_curso(curso)
    return jsonify(curso.dict())

@app.teardown_appcontext
def shutdown_event(exception=None):
    close_connection()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)