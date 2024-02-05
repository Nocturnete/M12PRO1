from . import api_bp
from .helper_auth import token_auth
from flask import current_app, request
from ..models import Order, ConfirmedOrder
from ..helper_json import json_response, json_request
from .errors import not_found, bad_request

@api_bp.route('/orders', methods=['POST'])
@token_auth.login_required
def create_order():
    try:
        data = request.get_json()
        buyer_id = token_auth.current_user().id
        data['buyer_id'] = buyer_id

        new_order = Order(**data)
        Order.save(new_order)
        return json_response({'order': new_order.to_dict()})
    except Exception as e:
        current_app.logger.error(e)
        return bad_request(str(e))
    
    
@api_bp.route('/orders/<order_id>', methods=['PUT'])
@token_auth.login_required
def update_order(order_id):
    try:
        order = Order.get(order_id)
        current_user_id = token_auth.current_user().id

        if not order:
            return not_found("Orden no encontrada")
        
        if order.buyer_id != current_user_id:
            return json_response({"message": "No tienes permisos para actualizar esta orden"})
        
        confirmed = ConfirmedOrder.get_filtered_by_confirmed(order)
        if confirmed:
            return json_response({"message": "No puedes eliminar una orden con oferta confirmada"})
        else:
            data = json_request(['offer'], False)
            order.update(**data)

        current_app.logger.debug("Updated order: {}".format(order.to_dict()))
        return json_response(order.to_dict())
    except Exception as e:
        current_app.logger.debug(e)
        return bad_request(str(e))
    

@api_bp.route('/orders/<order_id>', methods=['DELETE'])
@token_auth.login_required
def delete_order(order_id):
    try:
        order = Order.get(order_id)
        current_user_id = token_auth.current_user().id
        
        if not order:
            return not_found("Orden no encontrada")
        
        if order.buyer_id != current_user_id:
            return json_response({"message": "No tienes permisos para eliminar esta orden"})
        
        confirmed = ConfirmedOrder.get_filtered_by_confirmed(order)
        if confirmed:
            return json_response({"message": "No puedes eliminar una orden con oferta confirmada"})
        else:
            Order.delete(order)
            Order.remove(order)
            return json_response({'message': 'Orden eliminada exitosamente'})

    except Exception as e:
        current_app.logger.error(e)
        return bad_request(str(e))
