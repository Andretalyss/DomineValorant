from flask import Blueprint, request, jsonify
from psycopg2 import sql
import jwt, datetime
import psycopg2
import bcrypt
import re

from vars.variables import db_config, SECRET_TOKEN

auth_route = Blueprint('login', __name__)

def valida_senha(senha):
    padrao_senha = r'^(?=.*[A-Za-z0-9])(?=.*[@#$%^&+=])(?=\S+$).{8,}$'
    if re.match(padrao_senha, senha):
        return True
    else:
        return False

def validacao_emails(email):
    padrao_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(padrao_email, email):
        return True
    else:
        return False

### GERA TOKEN JWT COM UMA HORA DE EXPIRAÇÃO
def generate_jwt(id):
    payload = {
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_TOKEN, algorithm='HS512')
    return token

### REGISTRA NOVO USUÁRIO, PEDE USER E SENHA
@auth_route.route('/register', methods=['POST'], strict_slashes=False)
def register_new_user():
    data = request.get_json()

    if 'email' not in data:
        return jsonify({'mensagem': 'O campo "email" é obrigatório.'}), 400
    elif 'username' not in data:
        return jsonify({'mensagem': 'O campo "username" é obrigatório.'}), 400
    elif 'password' not in data:
        return jsonify({'mensagem': 'O campo "password" é obrigatório.'}), 400
    
    username = data['username']
    password = data['password']
    email    = data['email']

    if validacao_emails(email) == False:
       return jsonify({'mensagem': 'O campo "email" contém um email inválido.'}), 400
    
    if valida_senha(password) == False:
        return jsonify({
            'mensagem': 'A senha precisa ter pelo menos um número, um caractere especial e ter mais de 8 caracteres.'}), 400
    
    if len(username) < 6:
        return jsonify({
            'mensagem': 'O username precisa ter 6 caracteres ou mais.'}), 400
    
    encrypt_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db_connection = psycopg2.connect(**db_config)
    cursor = db_connection.cursor()
    
    db_query = sql.SQL("INSERT INTO users (username, password, email) VALUES ({}, {}, {})").format(
        sql.Literal(username),
        sql.Literal(encrypt_password.decode('utf-8')),
        sql.Literal(email)
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
@auth_route.route('/login', methods=['POST'],strict_slashes=False)
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    db_connection = psycopg2.connect(**db_config)
    cursor = db_connection.cursor()

    db_query = sql.SQL("SELECT id, password FROM users WHERE username = {}").format(
        sql.Literal(username)
    )
    try:    
        cursor.execute(db_query)
        row = cursor.fetchone()
        if row:
            db_password = row[1].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), db_password):
                token = generate_jwt(row[0])
                return jsonify({'Bearer': token})

        db_connection.close()
        return jsonify({'error': 'Invalid credentials.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
  
## AUTENTICA USUARIO, PEDINDO USER E SENHA E RETORNANDO TOKEN JWT
@auth_route.route('/login/recuperar-senha', methods=['POST'],strict_slashes=False)
def recuperar_acesso():
    data = request.get_json()
    email = data['email']

    if email:
        try:
            db_query = sql.SQL("SELECT id FROM users WHERE email = {}").format(sql.Literal(email))
            db_connection = psycopg2.connect(**db_config)
            cursor = db_connection.cursor()
            cursor.execute(db_query)
            row = cursor.fetchone()

            if row:
                token = generate_jwt(row[0])
                db_query = sql.SQL("UPDATE users SET token = {} where id = {}").format(sql.Literal(token), sql.Literal(row[0]))

                try:
                    cursor.execute(db_query)
                    db_connection.commit()
                    
                    # CÓDIGO AQUI DE ENVIO DE TOKEN PARA EMAIL
                    ###
                    ###    
                    ###
                    return jsonify({'message': 'Email enviado com instruções de recuperação de senha.'}), 200
                except Exception as e:
                    return jsonify({'error': str(e)}), 400

            else:
                return jsonify({'error': 'Token válido porém não pertence ao usuário'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'Campo email não informado.'})


## ALTERA SENHA DE USUARIO BASEADO NO TOKEN ENVIADO PARA ELE E ARMAZENADO NO BANCO DE DADOS.
@auth_route.route('/login/altera-senha', methods=['POST'],strict_slashes=False)
def alterar_senha():
    token_recuperacao = request.args.get('token')
    data = request.get_json()
    new_password = data['password']

    if token_recuperacao:
        try:
            payload = jwt.decode(token_recuperacao, SECRET_TOKEN, algorithms=['HS512'])
            user_id = payload['user_id']
            db_connection = psycopg2.connect(**db_config)
            cursor = db_connection.cursor()
            
            db_query = sql.SQL("SELECT token FROM users WHERE id = {}").format(sql.Literal(user_id))

            try:
                cursor.execute(db_query)
                row = cursor.fetchone()

                if row:
                    if row[0] != token_recuperacao:
                        return jsonify({'error': 'Token inválido'})
                else:
                    return jsonify({'error': 'Token válido porém não pertence ao usuário'})
            except Exception as e:
                return jsonify({'error': str(e)}), 400
            
            encrypt_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

            db_query = sql.SQL("UPDATE users SET password = {} where id = {}").format(
                sql.Literal(encrypt_password.decode('utf-8')),
                sql.Literal(user_id)
            )

            try:
                cursor.execute(db_query)
                db_connection.commit()

                db_query = sql.SQL("UPDATE users SET token = {} WHERE id = {}").format(sql.Literal(None), sql.Literal(user_id))
                try:
                    cursor.execute(db_query)
                    db_connection.commit()
                    db_connection.close()
                    return jsonify({'message': 'Senha alterada.'})
                except Exception as e:
                    return jsonify({'error': str(e)}), 400
            except Exception as e:
                return jsonify({'error': str(e)}), 400
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado.'})
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido.'})   
    else:
        return jsonify({'error': 'Token inválido ou expirado.'})