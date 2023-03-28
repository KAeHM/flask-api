from flask import Flask, request
from pymongo import MongoClient
from flask_bcrypt import Bcrypt 
import jwt


app = Flask(__name__)
client = MongoClient('mongodb://mongodb:27017')
db = client['flaskdb']
bcrypt = Bcrypt(app) 


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



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)