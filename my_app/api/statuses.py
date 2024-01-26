from . import api_bp
from ..models import Status
from ..helper_json import json_response
from .errors import bad_request
from flask import current_app

# List
@api_bp.route('/statuses', methods=['GET'])
def get_statuses():
    try:
        statuses = Status.get_all()
        print("Longitud de statuses:", len(statuses))
        data = Status.to_dict_collection(statuses)
    except Exception as e:
        current_app.logger.error(e)
        return bad_request(str(e))
    else:
        return json_response(data)
