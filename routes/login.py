from flask import Blueprint, request, jsonify
from psycopg2 import sql
import jwt, datetime
import psycopg2
import bcrypt

from vars.variables import db_config, SECRET_TOKEN

auth_route = Blueprint('login', __name__)

### GERA TOKEN JWT COM UMA HORA DE EXPIRAÇÃO
def generate_jwt(id):
    payload = {
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_TOKEN, algorithm='HS512')
    return token

### REGISTRA NOVO USUÁRIO, PEDE USER E SENHA
@auth_route.route('/register', methods=['POST'])
def register_new_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    encrypt_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db_connection = psycopg2.connect(**db_config)
    cursor = db_connection.cursor()
    
    db_query = sql.SQL("INSERT INTO users (username, password) VALUES ({}, {})").format(
        sql.Literal(username),
        sql.Literal(encrypt_password.decode('utf-8'))
    )

    try:
        cursor.execute(db_query)
        db_connection.commit()
        return jsonify({'message': "User added with success"}), 200
    except Exception as e:
        db_connection.rollback()
        return jsonify({'Error': str(e)}), 400
    finally:
        db_connection.close()
        
    
## AUTENTICA USUARIO, PEDINDO USER E SENHA E RETORNANDO TOKEN JWT
@auth_route.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    db_connection = psycopg2.connect(**db_config)
    cursor = db_connection.cursor()

    db_query = sql.SQL("SELECT id, password FROM users WHERE username = {}").format(
        sql.Literal(username)
    )

    cursor.execute(db_query)
    row = cursor.fetchone()

    if row:
        db_password = row[1].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), db_password):
            token = generate_jwt(row[0])
            return jsonify({'Bearer': token})
    
    db_connection.close()
    return jsonify({'error': 'Invalid credentials.'})