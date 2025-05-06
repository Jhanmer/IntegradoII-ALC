from flask import Blueprint, render_template, request, redirect, url_for
from app.config import get_db_connection  

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('pages-profile.html')

@main.route('/sign-in')
def sign_in():
    return render_template('pages-sign-in.html')

@main.route('/sign-up')
def sign_up():
    return render_template('pages-sign-up.html')

@main.route('/error')
def error():
    return render_template('pages-blank.html')

@main.route('/ui-buttons', methods=['GET', 'POST'])
def ui_buttons():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            descripcion = request.form['descripcion']
            sku = request.form['sku']
            marca = request.form['marca']
            proveedor = request.form['proveedor']
            division = request.form['division']
            estado = request.form['estado'].lower() == 'activo'
            oh_disponible = int(request.form['oh_disponible'])
            nuevo_oh = int(request.form['nuevo_oh'])

            # Insertar en base de datos
            cur.execute("""
                INSERT INTO productos (descripcion, sku, marca, proveedor, division, estado, oh_disponible, nuevo_oh)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (descripcion, sku, marca, proveedor, division, estado, oh_disponible, nuevo_oh))

            conn.commit()
            return redirect(url_for('main.ui_buttons'))

        except Exception as e:
            print("Error al insertar producto:", e)

    # Mostrar todos los productos
    cur.execute("SELECT * FROM productos ORDER BY id DESC")
    productos = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('ui-buttons.html', productos=productos)
