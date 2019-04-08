from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import json
from flask_cors import CORS
import bitso
api = bitso.Api("UoYaFpZTGI", "57baffae5d1e57e224d692acfa9b154a")


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

blacklist = set()

users = [
    User(1, 'jorge', 'jorge'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    print(username, password)
    user = username_table.get(username, None)
    print (user)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

def getFees(app):
    if app == "bitso":
        return api.fees()
    else:
        pass

def sum(a,b):
    return a+b

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
cors = CORS(app, resources={r"/auth": {"origins": "*"}})
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

@app.route('/fees', methods=['GET'])
def fees():
    app = request.args.get('app')
    fees = getFees(app)
    print(fees.btc_mxn.fee_percent)
    return jsonify({"jaja":"jeje"})

@app.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    idval = len(users)+1
    user = User(idval, data['username'], data['password'])
    users.append(user)
    username_table = {u.username: u for u in users}
    userid_table = {u.id: u for u in users}
    return jsonify({"msg": "Successfully register"}), 200

@app.route('/list', methods=['GET'])
def list():
    books = api.balances()
    print("viendo books")
    print (books)
    userList = []
    for x in users:
        userList.append({"user": x.username, "pass": x.password})
    return jsonify({"msg": userList}), 200

@app.route('/protected')
@jwt_required()
def protected():
    ticker = api.account_status()
    print("viendo tiker")
    print(ticker)
    return '%s' % dir(current_identity)

@app.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    blacklist.add(current_identity)
    return jsonify({"msg": "Successfully logged out"}), 200



if __name__ == '__main__':
    app.run()
