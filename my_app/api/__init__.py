from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import categories, products, orders, statuses, users, confirmed_orders, tokens

