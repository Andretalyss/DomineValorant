### Utilizar quando for popular banco de dados com agentes
# def agents_info_get_all():
#     url = "https://valorant-api.com/v1/agents?language=pt-BR"
#     response = requests.get(url)

#     db_connection = psycopg2.connect(**db_config)
#     cursor = db_connection.cursor()

#     if response.status_code == 200:
#         data = response.json()

#         for j in range(10,23):
#             agent_name = data['data'][j]['displayName']
#             agent_function = data['data'][j]['role']['displayName']
#             ability1_name = data['data'][j]['abilities'][0]['displayName']
#             ability1_description = data['data'][j]['abilities'][0]['description']        
#             ability2_name = data['data'][j]['abilities'][1]['displayName']
#             ability2_description = data['data'][j]['abilities'][1]['description']  
#             ability3_name = data['data'][j]['abilities'][2]['displayName']
#             ability3_description = data['data'][j]['abilities'][2]['description']
#             ultimate_name = data['data'][j]['abilities'][3]['displayName']
#             ultimate_description = data['data'][j]['abilities'][3]['description'] 

#             db_query = sql.SQL("""INSERT INTO agents (agent_name, agent_function, ability1_name, ability1_description, ability2_name, ability2_description, ability3_name, ability3_description, ultimate_name, ultimate_description)
#                 values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}) 
#             """).format(
#                 sql.Literal(agent_name),
#                 sql.Literal(agent_function),
#                 sql.Literal(ability1_name),
#                 sql.Literal(ability1_description),
#                 sql.Literal(ability2_name),
#                 sql.Literal(ability2_description),
#                 sql.Literal(ability3_name),
#                 sql.Literal(ability3_description),
#                 sql.Literal(ultimate_name),
#                 sql.Literal(ultimate_description)
#             )

            
#             cursor.execute(db_query)
#             db_connection.commit()
                

#         return jsonify({'banco populado'}), 200