from flask import Blueprint, jsonify
from psycopg2 import sql
import psycopg2
import redis
import pickle

from vars.variables import db_config, REDIS_HOST, REDIS_DB, REDIS_PORT

agents_info_routes = Blueprint('agents', __name__)

### RETORNA TODOS OS AGENTES
@agents_info_routes.route('/agents', methods=['GET'],strict_slashes=False)
def agents_info_get_all():
    redis_connection = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    if redis_connection.exists('agents_all'):
        data = redis_connection.get('agents_all')
        data = pickle.loads(data)
        json_data = jsonify(data)
        json_data.headers['Content-Type'] = 'application/json; charset=utf-8'
        return json_data, 200
    else:
        db_connection = psycopg2.connect(**db_config)
        cursor = db_connection.cursor()

        db_query = sql.SQL("""
            SELECT * FROM agents
        """)

        cursor.execute(db_query)
        result = cursor.fetchall()
        json_data = []
        for row in result:
            json_data.append({
                "Nome": row[0],
                "Função": row[1],
                "Habilidade 1": {
                    "Nome": row[2],
                    "Descrição": row[3]
                },
                "Habilidade 2": {
                    "Nome": row[4],
                    "Descrição": row[5]
                },
                "Habilidade 3": {
                    "Nome": row[6],
                    "Descrição": row[7]
                },
                "Ultimate": {
                    "Nome": row[8],
                    "Descrição": row[9]
                }
            })

        redis_data = pickle.dumps(json_data)
        redis_connection.set('agents_all', redis_data, 300)
        json_data = jsonify(json_data)
        json_data.headers['Content-Type'] = 'application/json; charset=utf-8'
        
        return json_data, 200

### RETORNA AGENTE POR NOME
@agents_info_routes.route('/agents/<agent>', methods=['GET'],strict_slashes=False)
def agent_get(agent):
    redis_connection = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    if redis_connection.exists(f'{agent}-info'):
        data = redis_connection.get(f'{agent}-info')
        data = pickle.loads(data)
        json_data = jsonify(data)
        json_data.headers['Content-Type'] = 'application/json; charset=utf-8'
        return json_data, 200
    else:
        db_connection = psycopg2.connect(**db_config)
        cursor = db_connection.cursor()

        db_query = sql.SQL("""
            SELECT agent_function, ability1_name, ability1_description, ability2_name, ability2_description, ability3_name, ability3_description, ultimate_name, ultimate_description FROM agents WHERE agent_name = {}                  
        """).format(sql.Literal(agent))

        cursor.execute(db_query)
        row = cursor.fetchone()

        if row:
            data = {
                "Nome": agent,
                "Função": row[0],
                "Habilidade 1": {
                    "Nome": row[1],
                    "Descrição": row[2]
                },
                "Habilidade 2": {
                    "Nome": row[3],
                    "Descrição": row[4]
                },
                "Habilidade 3": {
                    "Nome": row[5],
                    "Descrição": row[6]
                },
                "Ultimate": {
                    "Nome": row[7],
                    "Descrição": row[8]
                }
            }

            redis_data = pickle.dumps(data)
            redis_connection.set(f'{agent}-info', redis_data, 100)
            json_data = jsonify(data)
            json_data.headers['Content-Type'] = 'application/json; charset=utf-8'
            return json_data, 200
        
        db_connection.close()
        return jsonify({'error': "Agent not found"}), 404
