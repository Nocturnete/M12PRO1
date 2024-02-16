from . import api_bp
from .errors import not_found, bad_request
from ..models import Product, Category, Order, User
from ..helper_json import json_request, json_response
from flask import current_app, request
from .helper_auth import token_auth

# List
@api_bp.route('/products', methods=['GET'])
def get_products():
    search = request.args.get('title')
    if search:
        my_filter = Product.title.like('%' + search + '%')
        products_with_categories = Product.filter(my_filter)
    else:
        products_with_categories = Product.get_all_with(Category)
    data = Product.to_dict_collection(products_with_categories)
    return json_response(data)

# Read
@api_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    result = Product.get_with(id, Category)
    if result:
        (product, category) = result
        # Serialize data
        data = product.to_dict()
        # Add relationship
        data["category"] = category.to_dict()
        del data["category_id"]
        return json_response(data)
    else:
        current_app.logger.debug("Item {} not found".format(id))
        return not_found("Item not found")
    
# Update
@api_bp.route('/products/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_product(id):
    product = Product.get(id)
    user = User.get_one_filtered(id=product.seller_id)
    user_current = token_auth.current_user().id
    if user.id == user_current:
        if product:
            try:
                data = json_request(['title', 'description', 'photo', 'price', 'category_id', 'status_id'], False)
            except Exception as e:
                current_app.logger.debug(e)
                return bad_request(str(e))
            else:
                product.update(**data)
                current_app.logger.debug("UPDATED product: {}".format(product.to_dict()))
                return json_response(product.to_dict())
        else:
            current_app.logger.debug("Product {} not found".format(id))
            return not_found("Product not found")
    else:
        return not_found("Permission denied")

# List
@api_bp.route('/products/<int:id>/orders', methods=['GET'])
def get_orders(id):
    orders = Order.get_all_filtered_by(product_id=id)
    data = Category.to_dict_collection(orders)
    return json_response(data)