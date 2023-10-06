from flask import Flask, flash, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
from datetime import datetime
import sqlite3
import os

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "xxx"

# ------------------------------------------------------------------
# |                           FUNCIONES                            |
# ------------------------------------------------------------------
def allowed_file(photoname):
    return '.' in photoname and photoname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# ------------------------------------------------------------------
# |                         BASE DE DATOS                          |
# ------------------------------------------------------------------
DATABASE = 'database.db'

def get_db():
    db = getattr(Flask, '_database', None)
    if db is None:
        db = Flask._database = sqlite3.connect(DATABASE,check_same_thread=False)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    db = getattr(Flask, '_database', None)
    if db is not None:
        db.close()

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
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM products")
    productos = cursor.fetchall()
    cursor.close()
    return render_template("products/list.html", producto=productos)

# ------------------------------------------------------------------
# |                          create.html                           |
# ------------------------------------------------------------------
@app.route("/products/create", methods=["GET", "POST"])
def products_create():
    if request.method == "GET":
        cursor = get_db().cursor()
        cursor.execute("SELECT id, name FROM categories")
        categorias = cursor.fetchall()
        cursor.close()
        return render_template("products/create.html", categoria=categorias)
    elif request.method == "POST":
        title = request.form["nombre"]
        description = request.form["descripcion"]
        photo = request.files['imagen']
        price = request.form["precio"]
        category_id = request.form["categoria"]
        seller_id = 1
        fecha = datetime.now()
        created = fecha.strftime("%Y/%m/%d %H:%M:%S")
        updated = fecha.strftime("%Y/%m/%d %H:%M:%S")
        if not title or len(title) > 255:
            flash("Nombre : no puede estar vacío y no debe superar los 255 caracteres.", 'error')
        if not description:
            flash("Descripción : no puede estar vacío.", 'error')
        if not photo or photo.filename == '':
            flash("No se ha seleccionado ninguna imagen", 'error')
        max_file_size = 2 * 1024 * 1024
        if len(photo.read()) > max_file_size:
            flash("El archivo de imagen supera el tamaño máximo permitido de 2MB.", 'error')
        if allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash("Formato de archivo no permitido. Por favor, elige una imagen válida.", 'error')
        if not price:
            flash("Precio : no puede estar vacío.", 'error')
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO products(title, description, photo, price, category_id, seller_id, created, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(title, description, photo, price, category_id, seller_id, created, updated))
            conn.commit()
            flash("Producto creado con éxito", 'success')
            return redirect(url_for("products_list"))
        except Exception as e:
            conn.rollback()
            flash("Error en la creación del producto.", 'error')
            return redirect(url_for("products_create"))
        finally:
            cursor.close()

# ------------------------------------------------------------------
# |                          update.html                           |
# ------------------------------------------------------------------
@app.route("/products/update/<int:id>", methods=["GET", "POST"])
def products_update(id):
    if request.method == "GET":
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?",(id,))
        producto = cursor.fetchone()
        cursor.execute("SELECT id, name FROM categories")
        categorias = cursor.fetchall()
        cursor.close()
        return render_template("products/update.html", dato=producto, categoria=categorias)
    elif request.method == "POST":
        title = request.form["nombre"]
        description = request.form["descripcion"]
        photo = request.form["imagen"]
        price = request.form["precio"]
        category_id = request.form["categoria"]
        seller_id = 1 
        fecha = datetime.now()
        updated = fecha.strftime("%Y/%m/%d %H:%M:%S")
        if not title or len(title) > 255:
            flash("Nombre : no puede estar vacío y no debe superar los 255 caracteres.", 'error')
        if not description:
            flash("Descripción : no puede estar vacío.", 'error')
        if not photo or photo.filename == '':
            flash("No se ha seleccionado ninguna imagen", 'error')
        max_file_size = 2 * 1024 * 1024
        if len(photo.read()) > max_file_size:
            flash("El archivo de imagen supera el tamaño máximo permitido de 2MB.", 'error')
        if allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash("Formato de archivo no permitido. Por favor, elige una imagen válida.", 'error')
        if not price:
            flash("Precio : no puede estar vacío.", 'error')
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE products SET title=?, description=?, photo=?, price=?, category_id=?, seller_id=?, updated=? WHERE id=?", (title, description, photo, price, category_id, seller_id, updated, id))
            conn.commit()
            flash("Producto modificado con éxito", 'success')
            return redirect(url_for("products_list"))
        except Exception as e:
            conn.rollback()
            flash("Error en la modificación del producto.", 'error')
            return redirect(url_for("products_update"))
        finally:
            cursor.close()



# ------------------------------------------------------------------
# |                           read.html                            |
# ------------------------------------------------------------------
@app.route("/products/read/<int:id>")
def products_read(id):
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM products WHERE id=?", (id,))
    producto = cursor.fetchone()
    cursor.close()
    return render_template("products/read.html", dato=producto)

# ------------------------------------------------------------------
# |                          delete.html                           |
# ------------------------------------------------------------------
@app.route("/products/delete/<int:id>", methods=["GET", "POST"])
def products_delete(id):
    if request.method == "GET":
        cursor = get_db().cursor()
        cursor.execute("SELECT * FROM products WHERE id=?", (id,))
        producto = cursor.fetchone()
        cursor.close()
        return render_template("products/delete.html", dato=producto)
    elif request.method == "POST":
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=?", (id,))
        conn.commit()
        cursor.close()
        return redirect(url_for("products_list"))

# ------------------------------------------------------------------
# |                   Web Flask Servidor Local                     |
# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)