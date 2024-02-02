from . import api_bp
from flask import current_app, request
from ..models import Order
from ..helper_json import json_response, json_request
from .errors import not_found, bad_request


@api_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = request.get_json()
        new_order = Order(**order_data)
        Order.save(new_order)
        return json_response({'order': new_order.to_dict()})
    except Exception as e:
        current_app.logger.error(e)
        return bad_request(str(e))

@api_bp.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        order = Order.get(order_id)
        if not order:
            return not_found("Orden no encontrada")

        data = json_request(['offer'], False)
        order.update(**data)

        current_app.logger.debug("Updated order: {}".format(order.to_dict()))
        return json_response(order.to_dict())
    except Exception as e:
        current_app.logger.debug(e)
        return bad_request(str(e))
    

@api_bp.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        order = Order.get(order_id)
        if not order:
            return not_found("Orden no encontrada")
        
        Order.delete(order)

        return json_response({'message': 'Orden eliminada exitosamente'})
    except Exception as e:
        current_app.logger.error(e)
        return bad_request(str(e))
    finally:
        Order.remove(order)