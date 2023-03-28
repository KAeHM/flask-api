from flask import Flask, request
from pymongo import MongoClient
from flask_bcrypt import Bcrypt 
import xml.etree.ElementTree as ET
import jwt
import requests
import json


app = Flask(__name__)
client = MongoClient('mongodb://mondodb:27017')
db = client['flaskdb']
bcrypt = Bcrypt(app) 


def search_city(cep):
    api_request = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    formated_data = json.loads(api_request.content)
    return formated_data['localidade']

def search_city_code(city):
    api_request = requests.get(f'http://servicos.cptec.inpe.br/XML/listaCidades?city={city}')
    root = ET.ElementTree(ET.fromstring(api_request.content))
    id = None
    for child in root.findall("cidade"):
        id = child.find("id").text
        break
    return id

def search_forecast(cep):
    city = search_city(cep)
    id = search_city_code(city)


    api_request = requests.get(f'http://servicos.cptec.inpe.br/XML/cidade/{id}/previsao.xml')
    root = ET.ElementTree(ET.fromstring(api_request.content))
    forecasts = []

    for child in root.findall('previsao'):
        dia = child.find('dia').text
        tempo = child.find('tempo').text
        maxima = child.find('maxima').text
        minima = child.find('minima').text
        iuv = child.find('iuv').text

        new_forecast_obj = {"day": dia, "weather": tempo, "max": maxima, "min": minima, 'iuv': iuv}
        forecasts.append(new_forecast_obj)
    return forecasts


@app.post('/users')
def create_users():
    data = request.json

    try:
        hash_password = bcrypt.generate_password_hash(data['password'])
        name = data['name']

        new_user = {"name": name, "password": hash_password}
        db.users.insert_one(new_user)
        return {"message": "sucess add to database", "user": {"name": name, "password": hash_password.decode()}}
    except:
        return {"message": 'this data is not valid, see the documentation for more information.'}, 401
    
@app.post('/login')
def acess_token():
    data = request.json
    user = db.users.find_one({'name': data['name']})

    if bcrypt.check_password_hash(user['password'], data['password']):
        payload = {
            "name": data['name']
        }
        secret = 'generic secret'
        token = jwt.encode(payload=payload, key=secret)
        return {'message': token}
    else:
        return {'message': 'invalid user or password'}

@app.post('/forecast')
def get_forecast():
    data = request.json
    cep = data['cep']

    forecasts = search_forecast(cep)
    return {'message': forecasts}



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)