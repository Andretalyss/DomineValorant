from flask import Blueprint, request, jsonify
import requests
from psycopg2 import sql
import psycopg2

from vars.variables import db_config

db_route = Blueprint('popule_db', __name__)

### Utilizar quando for popular banco de dados com agentes
@db_route.route('/popule', methods=['POST'], strict_slashes=False)
def agents_info_get_all():
    url = "https://valorant-api.com/v1/agents?language=pt-BR"
    response = requests.get(url)

    db_connection = psycopg2.connect(**db_config)
    cursor = db_connection.cursor()
    
    try:
        db_query = sql.SQL("""CREATE TABLE IF NOT EXISTS agents (
            agent_name varchar(15),
            agent_function varchar(15),
            ability1_name varchar(35),
            ability1_description varchar(500),
            ability2_name varchar(35),
            ability2_description varchar(500),
            ability3_name varchar(35),
            ability3_description varchar(500),
            ultimate_name varchar(35),
            ultimate_description varchar(500)  
        );""")

        cursor.execute(db_query)
        db_connection.commit()

        db_query = sql.SQL("""CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            username varchar(50) not null,
            password varchar(100) not null,
            email varchar(30) unique not null,
            token varchar(512)
        );""")

        cursor.execute(db_query)
        db_connection.commit()

    except Exception as e:
        return jsonify({'error': str(e)}), 400


    if response.status_code == 200:
        data = response.json()

        for j in range(0,23):
            if j == 9:
                continue
            agent_name = data['data'][j]['displayName']
            agent_function = data['data'][j]['role']['displayName']
            ability1_name = data['data'][j]['abilities'][0]['displayName']
            ability1_description = data['data'][j]['abilities'][0]['description']        
            ability2_name = data['data'][j]['abilities'][1]['displayName']
            ability2_description = data['data'][j]['abilities'][1]['description']  
            ability3_name = data['data'][j]['abilities'][2]['displayName']
            ability3_description = data['data'][j]['abilities'][2]['description']
            ultimate_name = data['data'][j]['abilities'][3]['displayName']
            ultimate_description = data['data'][j]['abilities'][3]['description'] 

            db_query = sql.SQL("""INSERT INTO agents (agent_name, agent_function, ability1_name, ability1_description, ability2_name, ability2_description, ability3_name, ability3_description, ultimate_name, ultimate_description)
                values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}) 
            """).format(
                sql.Literal(agent_name),
                sql.Literal(agent_function),
                sql.Literal(ability1_name),
                sql.Literal(ability1_description),
                sql.Literal(ability2_name),
                sql.Literal(ability2_description),
                sql.Literal(ability3_name),
                sql.Literal(ability3_description),
                sql.Literal(ultimate_name),
                sql.Literal(ultimate_description)
            )

            cursor.execute(db_query)
            db_connection.commit()

        db_connection.close()
        return jsonify({'message': 'banco populado'}), 200