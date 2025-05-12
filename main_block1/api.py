from flask import request, Blueprint
from database import Database
import json 

bp = Blueprint('api', __name__)
db = Database('database.db')

@bp.post('/api/register')
def api_register():
    req = request.get_json()
    print("Got register request: ", req['email'])
    user = db.find_user(req['email'])
    if user != None:
        return json.dumps({'status': 400, 'message': 'User exists'})
    
    db.add_user(req)
    return json.dumps({'status': 200, 'message': 'Created'})

@bp.post('/api/auth')
def api_auth():
    req = request.get_json()
    print("Got authorization request: ", req['email'])
    user = db.find_user(req['email'])
    if user == []:
        return json.dumps({'status': 400, 'message': 'User does not exist'})
    
    password_hash, token = user[3], user[4]
    if password_hash != req['password']:
        return json.dumps({'status': 400, 'message': 'Passwords do not match'})

    return json.dumps({'status': 200, 'message': 'Authorized', 'token': token})


