from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from pymongo import message
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.wrappers import response

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/pythonmongodb'
mongo = PyMongo(app)

@app.route('/users',methods=['POST'])
def create_user():
    # Receiving data
    username = request.json['username']#limao
    password = request.json['password']
    email = request.json['email']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert(
            {'username': username, 'email': email, 'password': hashed_password}
        )
        response = {
            'íd': str(id),
            'username': username,
            'password': hashed_password,
            'email' : email
        }
        return response
    else:
       return not_found()

    return {'message': 'received'}

@app.route ('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response (response, mimetype='application/json')

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response (response, mimetype="appplication/json")

@app.route('/users/<id>', methods=['DELETE'])
def delete_users(id):
    mongo.db.users.delete_one({'_id':ObjectId(id)})
    response = jsonify({'message': 'User' + id + 'was Deleted succesfully'})
    return response

@app.route('/users/<id>', methods = ['PUT'])
def update_user(id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set':{
            'username': username,
            'password': hashed_password,
            'email': email
        }})
        response = jsonify({'message': 'User' + id + 'was updated succefully'})
        return response

@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        
        'message': 'Resurce Not found:' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response
if __name__== "__main__":
    app.run(debug=True)