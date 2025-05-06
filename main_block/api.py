from flask import request, Blueprint
from database import Database
import sqlite3 as sql
import json 

bp = Blueprint('api', __name__)
db = Database('database.db')

@bp.post('/api/register')
def api_register():
    req = request.get_json()
    print("Got register request: ", req['email'])
    users = db.find_user(req['email'])
    if users != []:
        return json.dumps({'status': 400, 'message': 'User exists'})
    
    db.add_user(req)
#   TODO: Возвращать токен авторизации
    return json.dumps({'status': 200, 'message': 'Created'})

