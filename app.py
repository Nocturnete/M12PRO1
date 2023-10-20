from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "xxx"

# ------------------------------------------------------------------
# |                           FUNCIONES                            |
# ------------------------------------------------------------------
def allowed_file(photoname):
    return '.' in photoname and photoname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------------------------------------------------------
# |                           BASE DE DATOS                        |
# ------------------------------------------------------------------
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy()
db.init_app(app)



# CATEGORIES
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)

# USERS
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated  = db.Column(db.DateTime, nullable=False, default=datetime.now)

# PRODUCTS
class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created = db.Column(db.DateTime)
    updated  = db.Column(db.DateTime)

# ORDERS
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    __table_args__ = (db.UniqueConstraint('product_id', 'buyer_id', name='uc_product_buyer'),)

# CONFIRMED ORDERS
class Confirmed_Order(db.Model):
    __tablename__ = "confirmed_orders"
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)

# ------------------------------------------------------------------
# |                          index.html                            |
# ------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

# ------------------------------------------------------------------
# |                           list.html                            |
# ------------------------------------------------------------------
@app.route("/products/list")
def products_list():
    products_list = db.session.query(Product).order_by(Product.id.asc()).all()
    return render_template("products/list.html", products_list=products_list)

# ------------------------------------------------------------------
# |                          create.html                           |
# ------------------------------------------------------------------
@app.route("/products/create", methods=["GET", "POST"])
def products_create():
    if request.method == "GET":
        categories = db.session.query(Category).order_by(Category.id.asc()).all()
        return render_template("products/create.html", categories=categories)
    else:
        title = request.form["nombre"]
        description = request.form["descripcion"]
        photo = request.files['imagen']
        price = int(request.form["precio"])
        category_id = int(request.form["categoria"])
        seller_id = 1
        if not title or len(title) > 255:
            flash("Nombre : no puede estar vacío y no debe superar los 255 caracteres.", 'error')
        if not description:
            flash("Descripción : no puede estar vacío.", 'error')
        if not photo or photo.filename == '':
            flash("No se ha seleccionado ninguna imagen", 'error')
        max_file_size = 2 * 1024 * 1024
        if len(photo.read()) > max_file_size:
            flash("El archivo de imagen supera el tamaño máximo permitido de 2MB.", 'error')
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(file_path)
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
            return redirect(url_for("products_list"))
        else:
            flash("Formato de archivo no permitido. Por favor, elige una imagen válida.", 'error')
        if not price:
            flash("Precio : no puede estar vacío.", 'error')

# ------------------------------------------------------------------
# |                           read.html                            |
# ------------------------------------------------------------------
@app.route("/products/read/<int:Product_id>")
def products_read(Product_id):
    (product,categoria) = db.session.query(Product, Category).join(Category).filter(Product.id == Product_id).one()
    return render_template("products/read.html", products=product, categoria = categoria)

# ------------------------------------------------------------------
# |                          delete.html                           |
# ------------------------------------------------------------------
@app.route("/products/delete/<int:Product_id>", methods=["GET", "POST"])
def products_delete(Product_id):
    (product,categoria) = db.session.query(Product, Category).join(Category).filter(Product.id == Product_id).one()

    if request.method == 'GET':
        return render_template('products/delete.html', products=product, categoria = categoria)
    else:
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for("products_list"))

# ------------------------------------------------------------------
# |                          update.html                           |
# ------------------------------------------------------------------
@app.route("/products/update/<int:products_id>", methods=["GET", "POST"])
def products_update(products_id):
    product = db.session.query(Product).filter(Product.id == products_id).one()
    if request.method == 'GET':
        categories = db.session.query(Category).order_by(Category.id.asc()).all()
        return render_template("products/update.html", products=product, categories=categories)  
    elif request.method == 'POST':
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
            app.logger.debug("Imagen subida")
            max_file_size = 2 * 1024 * 1024
            if len(imagen.read()) > max_file_size:
                flash("El archivo de imagen supera el tamaño máximo permitido de 2MB.", 'error')
            elif allowed_file(photo.filename):
                app.logger.debug("Imagen valida")
                filename = secure_filename(imagen.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                imagen.save(file_path)
                product.photo = filename

        product.title = title
        product.description = description
        product.price = price
        product.category_id = category_id
        product.seller_id = seller_id
        product.updated = datetime.now()

        print(product.title)
        db.session.commit()

        flash("Producto actualizado con éxito", 'success')
        return redirect(url_for("products_list"))









# ------------------------------------------------------------------
# |                   Web Flask Servidor Local                     |
# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)