from flask import Blueprint, render_template, request
import psycopg2
from app.config import get_db_connection

main = Blueprint('main', __name__)

# Ruta principal
@main.route('/')
def index():
    return render_template('index.html')

# Ruta de inventario
@main.route('/inventario', methods=['GET', 'POST'])
def inventario():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.form
        cur.execute("""
            INSERT INTO productos (descripcion, sku, marca, proveedor, division, estado, oh_disponible, nuevo_oh)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['descripcion'], data['sku'], data['marca'],
            data['proveedor'], data['division'],
            data['estado'] == 'activo',
            data['oh_disponible'], data['nuevo_oh']
        ))
        conn.commit()

    cur.execute("SELECT * FROM productos ORDER BY id DESC")
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('inventario.html', productos=productos)
