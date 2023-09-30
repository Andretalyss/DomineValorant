from flask import Blueprint, jsonify
import requests

agents_info_routes = Blueprint('agents', __name__)

### RETORNA TODOS OS AGENTES
@agents_info_routes.route('/agents', methods=['GET'])
def agents_info_get_all():
    url = "https://valorant-api.com/v1/agents"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        lista_campos_to_delete = [
            "role", "recruitmentData", "voiceLine", "characterTags",
            "backgroundGradientColors", "background", "assetPath",
            "bustPortrait", "displayIcon", "displayIconSmall",
            "fullPortrait", "fullPortraitV2", "isAvailableForTest",
            "isBaseContent", "isFullPortraitRightFacing", "killfeedPortrait"
        ]
        
        flag = False
        for j in range(0,22): 
            for i in lista_campos_to_delete:
                display_name = data['data'][j]['displayName']
                if display_name == "Sova" and flag == False:
                    del data['data'][j]
                    flag = True
                    break

                del data['data'][j][f'{i}']
            
        return jsonify(data)
    else:
        return jsonify({'Error': 'Erro a acessar a api'}), 404
    
### RETORNA AGENTE POR NOME
@agents_info_routes.route('/agents/<agent>', methods=['GET'])
def agent_get(agent):
    url = "https://valorant-api.com/v1/agents"
    uid = ""
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for item in data['data']:
            if agent in item['displayName']:
                uid = item['uuid']
                break
    else:
        return jsonify({'Error': 'Erro a acessar a api'}), 404
    
    url = f"https://valorant-api.com/v1/agents/{uid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        lista_campos_to_delete = [
            "role", "recruitmentData", "voiceLine", "characterTags",
            "backgroundGradientColors", "background", "assetPath",
            "bustPortrait", "displayIcon", "displayIconSmall",
            "fullPortrait", "fullPortraitV2", "isAvailableForTest",
            "isBaseContent", "isFullPortraitRightFacing", "killfeedPortrait"
        ]

        for i in lista_campos_to_delete:
            del data['data'][f'{i}']

        data = data['data']
        return jsonify(data)
    else:
        return jsonify({'Error': 'Erro a acessar a api'}), 404