from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user
from werkzeug.utils import secure_filename
from .models import Product, Category, Status, Banned_Products
from .forms import ProductForm, DeleteForm
from .helper_role import Action, perm_required
import uuid
import os


products_bp = Blueprint("products_bp", __name__)

@products_bp.context_processor
def templates_processor():
    return {
        'Action': Action
    }

# ------------------------------------------------------------------
# |                           list.html                            |
# ------------------------------------------------------------------
@products_bp.route('/products/list')
@perm_required(Action.products_list)
def product_list():
    products_with_category = Product.get_all_with(Category)
    products_banned = Banned_Products.get_order_by_banned()
    categories = Category.get_order_by()
    products_banned_dict = {result.product_id: result.reason for result in products_banned}

    print("-----------")
    print(products_banned)
    print("-----------")
    return render_template('products/list.html', products_with_category = products_with_category, products_banned = products_banned_dict, categories = categories)

@products_bp.route('/products/banned/list')
@perm_required(Action.products_list)
def products_banned_list():
    # select amb join que retorna una llista de resultats
    products_with_category = Product.get_all_with(Category)
    products_banned = Banned_Products.get_order_by_banned()
    categories = Category.get_order_by()
    products_banned_list = [result.product_id for result in products_banned]

    return render_template('products/banned.html', products_with_category = products_with_category, products_banned = products_banned_list, categories = categories)

# ------------------------------------------------------------------
# |                          create.html                           |
# ------------------------------------------------------------------
@products_bp.route('/products/create', methods = ['POST', 'GET'])
@perm_required(Action.products_create)
def product_create(): 
    if current_user.blocked_user:
        flash('No puedes crear nuevos productos mientras estás bloqueado.', 'warning')
        return redirect(url_for('products_bp.product_list'))
    
    categories = Category.get_order_by()
    statuses = Status.get_order_by()

    form = ProductForm()
    form.category_id.choices = [(category.id, category.name) for category in categories]
    form.status_id.choices = [(status.id, status.name) for status in statuses]

    if form.validate_on_submit():
        new_product = Product()
        new_product.seller_id = current_user.id

        form.populate_obj(new_product)

        filename = __manage_photo_file(form.photo_file)
        if filename:
            new_product.photo = filename
        else:
            new_product.photo = "no_image.png"

        Product.save(new_product)

        flash("Se ha creado el producto", "success")

        return redirect(url_for('products_bp.product_list'))
    
    else:
        return render_template('products/create.html', form = form)

# ------------------------------------------------------------------
# |                           read.html                            |
# ------------------------------------------------------------------
@products_bp.route('/products/read/<int:product_id>')
@perm_required(Action.products_read)
def product_read(product_id):
    result = Product.get_all_with_tree_classes(Category, Status, id=product_id)
    if not result:
        abort(404)

    (product, category, status) = result
    return render_template('products/read.html', product = product, category = category, status = status)

# ------------------------------------------------------------------
# |                          update.html                           |
# ------------------------------------------------------------------
@products_bp.route('/products/update/<int:product_id>',methods = ['POST', 'GET'])
@perm_required(Action.products_update)
def product_update(product_id):
    product = Product.get_one_filtered(id=product_id)
    if not product:
        abort(404)

    if not current_user.is_action_allowed_to_product(Action.products_update, product):
        abort(403)

    categories = Category.get_order_by()
    statuses = Status.get_order_by()

    form = ProductForm(obj = product)
    form.category_id.choices = [(category.id, category.name) for category in categories]
    form.status_id.choices = [(status.id, status.name) for status in statuses]

    if form.validate_on_submit():
        form.populate_obj(product)

        filename = __manage_photo_file(form.photo_file)
        if filename:
            product.photo = filename

        Product.save(product)

        flash("Producto actualizado", "success")

        return redirect(url_for('products_bp.product_read', product_id = product_id))
    
    else:
        return render_template('products/update.html', product_id = product_id, form = form)

# ------------------------------------------------------------------
# |                          delete.html                           |
# ------------------------------------------------------------------
@products_bp.route('/products/delete/<int:product_id>',methods = ['GET', 'POST'])
@perm_required(Action.products_delete)
def product_delete(product_id):
    product = Product.get_one_filtered(id=product_id)

    if not product:
        abort(404)

    if not current_user.is_action_allowed_to_product(Action.products_delete, product):
        abort(403)

    form = DeleteForm()
    if form.validate_on_submit():
        Product.delete(product)

        flash("Producto borrado", "success")

        return redirect(url_for('products_bp.product_list'))

    else:
        return render_template('products/delete.html', form = form, product = product)


__uploads_folder = os.path.abspath(os.path.dirname(__file__)) + "/static/products/"

def __manage_photo_file(photo_file):
    if photo_file.data:
        filename = photo_file.data.filename.lower()

        if filename.endswith(('.png', '.jpg', '.jpeg')):
            unique_filename = str(uuid.uuid4())+ "-" + secure_filename(filename)
            photo_file.data.save(__uploads_folder + unique_filename)
            return unique_filename

    return None
