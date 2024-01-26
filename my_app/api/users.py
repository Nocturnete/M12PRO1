from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import User, Product
from ..helper_json import json_request, json_response
from flask import current_app, request

# List for name
@api_bp.route('/users', methods=['GET'])
def get_users():
    try:
        search = request.args.get('name')
        if search:
            my_filter = User.name.like('%' + search + '%')
            userFilter = User.filter(my_filter)
        else:
            userFilter = User.get_all()
        data = User.to_dict_collection(userFilter)
    except Exception as e:
        current_app.logger.error(e)
        return bad_request(str(e))
    else:
        return json_response(data)
    

# Show account public for id
@api_bp.route('/users/<user_id>', methods=['GET'])
def get_users_id(user_id):
    try:
        user = User.get_by_id(user_id)
        if user is None:
            return bad_request("Usuario no encontrado")
        data = user.to_dict()
    except Exception as e:
        current_app.logger.error(e)
        return bad_request(str(e))
    else:
        return json_response(data)
    
# List of products from account
@api_bp.route('/users/<user_id>/products', methods=['GET'])
def get_products_userId(user_id):
    try:
        user = User.get_by_id(user_id)
        if user is None:
            return bad_request("Usuario no encontrado")
        data = user.to_dict()
        products = Product.query.filter_by(seller_id=user.id).all()
        data['products'] = [product.to_dict() for product in products]

    except Exception as e:
        current_app.logger.error(e)
        return bad_request(str(e))
    else:
        return json_response(data)