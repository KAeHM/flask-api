from flask import Flask, request
from pymongo import MongoClient
from flask_bcrypt import Bcrypt 
from services import search_forecast, gen_logs
from swagger import swaggerui_blueprint
import jwt
import requests
import json


app = Flask(__name__)
app.register_blueprint(swaggerui_blueprint)
client = MongoClient('mongodb://mongodb:27017')
db = client['flaskdb']
bcrypt = Bcrypt(app)


@app.post('/users')
def create_users():
    try:
        data = request.json
        test_name = data['name']
        test_pass = data['password']
    except:
        output = {"message": 'this data is not valid, see the documentation for more information'}
        gen_logs(code=400, method='POST', output=output, input=data, message='past data is in invalid format')
        return output, 400

    user = db.users.find_one({'name': data['name']})
  
    if user:
       output = {"message": 'user alredy exists'}
       gen_logs(code=400, method='POST', output=output, input=data, message='data is alredy in database')
       return output, 400

    hash_password = bcrypt.generate_password_hash(data['password'])
    name = data['name']

    new_user = {"name": name, "password": hash_password}
    db.users.insert_one(new_user)
        
    output = {"message": "sucess add to database", "user": {"name": name, "password": hash_password.decode()}}
    gen_logs(code=400, method='POST', output=output, input=data, message='created a new user in database')
    return output, 201

@app.post('/login')
def acess_token():
    try:
        data = request.json
    except:
        output = {"message": 'this data is not valid, see the documentation for more information'}
        gen_logs(code=400, method='POST', output=output, input='None', message='past data is in invalid format')
        return output, 400
    
   
    user = db.users.find_one({'name': data['name']})
    
    if not user:
        output = {"message": 'user not exists'}
        gen_logs(code=400, method='POST', output=output, input='None', message='past data do not exists.')
        return output, 400

    if bcrypt.check_password_hash(user['password'], data['password']):
        payload = {
            "name": data['name']
        }
        secret = 'generic secret'
        token = jwt.encode(payload=payload, key=secret)

        output = {'message': token}
        gen_logs(code=200, method='POST', output=output, input='None', message='user pass at login.')
        return output, 200
    else:
        output = {'message': 'invalid user or password'}
        gen_logs(code=400, method='POST', output=output, input='None', message='past data is incorret.')
        return output, 401
    
@app.post('/forecast')
def get_forecast():
    try:
        data = request.json
        test_cep = data['cep']
    except:
        output = {"message": 'this data is not valid, see the documentation for more information.'}
        gen_logs(code=400, method='POST', output=output, input='None', message='past data is in invalid format.')
        return output, 400

    cep = data['cep']
    try:
        forecasts = search_forecast(cep)
    except:
        output = {"message": 'something went wrong.'}
        gen_logs(code=400, method='POST', output=output, input=data, message='something in external api going wrong.')
        return output, 400


    output = {'message': forecasts}
    gen_logs(code=200, method='POST', output=output, input=data, message='successful in forecast retrieve')
    return output, 200
    
@app.get('/logs')
def get_logs():
    data = requests.get("http://elasticsearch:9200/logs/_search")
    formatted_data = json.loads(data.content)
    return {"message": formatted_data}, 200

@app.get('/swagger')
def get_swagger():
    with open('src/static/configsw.json') as swaggerconfig:
        data = json.load(swaggerconfig)
      
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)