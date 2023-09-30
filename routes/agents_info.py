from flask import Blueprint, jsonify
import requests
import json
from psycopg2 import sql
import psycopg2

from vars.variables import db_config, SECRET_TOKEN

agents_info_routes = Blueprint('agents', __name__)

### RETORNA TODOS OS AGENTES
@agents_info_routes.route('/agents', methods=['GET'])
def agents_info_get_all():
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
    
    return json.dumps(json_data, ensure_ascii=False, indent=4)

### RETORNA AGENTE POR NOME
@agents_info_routes.route('/agents/<agent>', methods=['GET'])
def agent_get(agent):
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
        
        return json.dumps(data, ensure_ascii=False, indent=4), 200
    
    db_connection.close()
    return jsonify({'error': "Agent not found"}), 404
