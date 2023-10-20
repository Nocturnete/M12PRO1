from flask import flash, Blueprint, redirect, url_for, render_template, request, current_app
from .models import Category, User, Product, Order, Confirmed_Order
from werkzeug.utils import secure_filename
from . import db_manager as db
from datetime import datetime
import os

# Blueprint
main_bp = Blueprint("main_bp", __name__, template_folder="templates", static_folder="static/css")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
upload_folder = current_app.config['UPLOAD_FOLDER']

# ------------------------------------------------------------------
# |                           FUNCIONES                            |
# ------------------------------------------------------------------
def allowed_file(photoname):
    return '.' in photoname and photoname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------------------------------------------------------
# |                          index.html                            |
# ------------------------------------------------------------------
@main_bp.route('/')
def home():
    return redirect(url_for("main_bp.products_list"))

# ------------------------------------------------------------------
# |                           list.html                            |
# ------------------------------------------------------------------
@main_bp.route("/products/list")
def products_list():
    try:
        products_list = db.session.query(Product).order_by(Product.id.asc()).all()
        return render_template("list.html", products_list=products_list)
    except Exception:
        flash("No se han podido mostrar los productos.",'error') 
        return redirect(url_for("main_bp.products_list"))

# ------------------------------------------------------------------
# |                          create.html                           |
# ------------------------------------------------------------------
@main_bp.route("/products/create", methods=["GET", "POST"])
def products_create():
    if request.method == "GET":
        categories = db.session.query(Category).order_by(Category.id.asc()).all()
        return render_template("create.html", categories=categories)
    else:
        try:
            title = request.form["nombre"]
            if not title or len(title) > 255:
                flash("Nombre : No puede estar vacío y no debe superar los 255 caracteres.", 'error')
            description = request.form["descripcion"]
            if not description:
                flash("Descripción : No puede estar vacío.", 'error')
            price = int(request.form["precio"])
            if not price:
                flash("Precio : No puede estar vacío.", 'error')
            category_id = int(request.form["categoria"])
            seller_id = 1
            photo = request.files['imagen']
            max_file_size = 2 * 1024 * 1024
            if not photo or photo.filename == '':
                flash("Imagen : No se ha seleccionado ninguna imagen", 'error')
                if len(photo.read()) > max_file_size:
                   flash("Imagen : El archivo de imagen supera el tamaño máximo permitido de 2MB.", 'error')
            if photo and allowed_file(photo.filename):
                filename = secure_filename(photo.filename)
                file_path = os.path.join(upload_folder, filename)
                photo.save(file_path)
            else:
                flash("Formato de archivo no permitido.", 'error')  
            nuevo_producto = Product()
            nuevo_producto.title = title
            nuevo_producto.description = description
            nuevo_producto.photo = filename
            nuevo_producto.price = price
            nuevo_producto.category_id = category_id
            nuevo_producto.seller_id = seller_id
            nuevo_producto.created = datetime.now()
            nuevo_producto.updated = datetime.now()
            db.session.add(nuevo_producto)
            db.session.commit()
            flash("Producto creado.") 
            return redirect(url_for("main_bp.products_list"))
        except Exception:
            flash("No se ha podido crear el producto.",'error') 
            return redirect(url_for("main_bp.products_list"))

# ------------------------------------------------------------------
# |                           read.html                            |
# ------------------------------------------------------------------
@main_bp.route("/products/read/<int:Product_id>")
def products_read(Product_id):
    try:
        (product,categoria) = db.session.query(Product, Category).join(Category).filter(Product.id == Product_id).one()
        photo_name = product.photo
        return render_template("read.html", products=product, categoria = categoria, photo_name=photo_name)
    except Exception:
        flash("No se ha podido mostrar los datos del producto.",'error') 
        return redirect(url_for("main_bp.products_list"))

# ------------------------------------------------------------------
# |                          delete.html                           |
# ------------------------------------------------------------------
@main_bp.route("/products/delete/<int:Product_id>", methods=["GET", "POST"])
def products_delete(Product_id):
    (product,categoria) = db.session.query(Product, Category).join(Category).filter(Product.id == Product_id).one()
    if request.method == 'GET':
        return render_template('delete.html', products=product, categoria = categoria)
    else:
        try:
            db.session.delete(product)
            db.session.commit()
            return redirect(url_for("main_bp.products_list"))
        except Exception:
            flash("No se ha podido borrar los datos del producto.",'error') 
            return redirect(url_for("main_bp.products_list"))

# ------------------------------------------------------------------
# |                          update.html                           |
# ------------------------------------------------------------------
@main_bp.route("/products/update/<int:products_id>", methods=["GET", "POST"])
def products_update(products_id):
    product = db.session.query(Product).filter(Product.id == products_id).one()
    photo_name = product.photo
    if request.method == 'GET':
        categories = db.session.query(Category).order_by(Category.id.asc()).all()
        return render_template("update.html", products=product, categories=categories, photo_name=photo_name)  
    elif request.method == 'POST':
        try:
            title = request.form["nombre"]
            description = request.form["descripcion"]
            photo = request.files['imagen']
            price = request.form["precio"]
            category_id = int(request.form["categoria"])
            seller_id = 1
            imagen = request.files["imagen"]
            if not title or len(title) > 255:
                flash("Nombre: no puede estar vacío y no debe superar los 255 caracteres.", 'error')
            if not description:
                flash("Descripción: no puede estar vacío.", 'error')
            if not price:
                flash("Precio: no puede estar vacío.", 'error')
            if not photo or photo.filename == '':
                flash("No se ha seleccionado ninguna imagen", 'error')
            else:
                filename = photo.filename
                max_file_size = 2 * 1024 * 1024
                if len(imagen.read()) > max_file_size:
                    flash("El archivo de imagen supera el tamaño máximo permitido de 2MB.", 'error')
                elif allowed_file(photo.filename):
                    filename = secure_filename(imagen.filename)
                    file_path = os.path.join(upload_folder, filename)                
                    imagen.save(file_path)
                    product.photo = filename
            product.title = title
            product.description = description
            product.price = price
            product.category_id = category_id
            product.seller_id = seller_id
            product.updated = datetime.now()
            db.session.commit()
            flash("Producto actualizado con éxito", 'success')
            return redirect(url_for("main_bp.products_list"))
        except Exception:
            flash("No se ha podido actualizar el producto.",'error') 
            return redirect(url_for("main_bp.products_list"))