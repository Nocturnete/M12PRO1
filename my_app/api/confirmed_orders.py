from . import api_bp
from .errors import not_found, bad_request
from ..models import Order, ConfirmedOrder
from ..helper_json import json_request, json_response

@api_bp.route('/orders/<int:id>/confirmed', methods=['POST'])
def confirm_order(id):
    
    existing_confirmation = ConfirmedOrder.query.filter_by(order_id=id).first()
    if existing_confirmation:
        return json_response(existing_confirmation.to_dict())  

    order = Order.get(id)

    if order:
        try:
            new_confirm = ConfirmedOrder()
            new_confirm.order_id=id
            confirmed_order = ConfirmedOrder.save(new_confirm)
            return json_response(confirmed_order.to_dict())
        except Exception as e:

            return bad_request(str(e))
    else:
        return not_found("Order not found")
        
@api_bp.route('/orders/<int:id>/confirmed', methods=['DELETE'])
def confirm_order_delete(id):

    order = ConfirmedOrder.get(id)

    if order:
        try:
            confirmed_order = ConfirmedOrder.delete(order)
            return json_response({"message": "ConfirmedOrder deleted successfully"})
        except Exception as e:
            return bad_request(str(e))
    else:
        return not_found("ConfirmedOrder not found")