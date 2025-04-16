from flask import request, Blueprint
import json 

bp = Blueprint('api', __name__)

@bp.post('/api/register')
def api_register():
    print("Got register request: ", request.get_json())
    return json.dumps("Accepted")

