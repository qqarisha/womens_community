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
        return json.dumps({'status': 400, 'message': 'Пользователь с таким email уже существует.'})
    
    db.add_user(req)
    return json.dumps({'status': 200, 'message': 'Created'})

@bp.post('/api/auth')
def api_auth():
    req = request.get_json()
    print("Got authorization request: ", req['email'])
    user = db.find_user(req['email'])
    if user == None:
        return json.dumps({'status': 400, 'message': 'Пользователя не существует.'})
    
    password_hash, token = user[3], user[4]
    if password_hash != req['password']:
        print("Passwords do not match\n")
        return json.dumps({'status': 400, 'message': 'Пароли не совпадают.'})
    
    print("Popa")
    return json.dumps({
        'status': 200, 
        'message': 'Authorized', 
        'token': token
        })


