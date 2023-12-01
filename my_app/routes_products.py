from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user
from werkzeug.utils import secure_filename
from .models import Product, Category, Status
from .forms import ProductForm, DeleteForm
from .helper_role import Action, perm_required
from . import db_manager as db, mail_manager as mail, logger
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
    products_with_category = db.session.query(Product, Category).join(Category).order_by(Product.id.asc()).all()
    logger.debug(f"products_with_category = {products_with_category}")

    return render_template('products/list.html', products_with_category = products_with_category)

# ------------------------------------------------------------------
# |                          create.html                           |
# ------------------------------------------------------------------
@products_bp.route('/products/create', methods = ['POST', 'GET'])
@perm_required(Action.products_create)
def product_create(): 
    if current_user.blocked_user:
        flash('No puedes crear nuevos productos mientras estás bloqueado.', 'warning')
        return redirect(url_for('products_bp.product_list'))
    
    categories = db.session.query(Category).order_by(Category.id.asc()).all()
    statuses = db.session.query(Status).order_by(Status.id.asc()).all()

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

        db.session.add(new_product)
        db.session.commit()

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
    result = db.session.query(Product, Category, Status).join(Category).join(Status).filter(Product.id == product_id).one_or_none()

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
    product = db.session.query(Product).filter(Product.id == product_id).one_or_none()
    
    if not product:
        abort(404)

    if not current_user.is_action_allowed_to_product(Action.products_update, product):
        abort(403)

    categories = db.session.query(Category).order_by(Category.id.asc()).all()
    statuses = db.session.query(Status).order_by(Status.id.asc()).all()

    form = ProductForm(obj = product)
    form.category_id.choices = [(category.id, category.name) for category in categories]
    form.status_id.choices = [(status.id, status.name) for status in statuses]

    if form.validate_on_submit():
        form.populate_obj(product)

        filename = __manage_photo_file(form.photo_file)
        if filename:
            product.photo = filename

        db.session.add(product)
        db.session.commit()

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
    product = db.session.query(Product).filter(Product.id == product_id).one_or_none()

    if not product:
        abort(404)

    if not current_user.is_action_allowed_to_product(Action.products_delete, product):
        abort(403)

    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(product)
        db.session.commit()

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
