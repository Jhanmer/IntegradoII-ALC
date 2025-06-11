# app/routes/producto.py

from flask import Blueprint, render_template, request, redirect, url_for
from app.models import producto as producto_model 

producto_bp = Blueprint('producto', __name__, url_prefix='/productos')

@producto_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            datos = (
                request.form['descripcion'],
                request.form['sku'],
                int(request.form['marca']),         # ID
                request.form['proveedor'],          # Texto
                request.form['division'],           # Texto
                request.form['estado'].lower() == 'activo',
                int(request.form['oh_disponible']),
                int(request.form['nuevo_oh'])
            )
            producto_model.insertar(datos)
            return redirect(url_for('producto.index'))
        except Exception as e:
            print("Error al insertar producto:", e)
    productos_lista = producto_model.obtener_todos()
    marcas_lista = producto_model.obtener_marcas()
    return render_template('Productos.html', productos=productos_lista, marcas=marcas_lista)


@producto_bp.route('/agregar_marca', methods=['POST'])
def agregar_marca():
    nombre = request.form['nueva_marca']
    producto_model.insertar_marca(nombre)
    return redirect(url_for('producto.index'))
