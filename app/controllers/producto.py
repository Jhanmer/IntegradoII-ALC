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
                request.form['marca'],
                request.form['proveedor'],
                request.form['division'],
                request.form['estado'].lower() == 'activo',
                int(request.form['oh_disponible']),
                int(request.form['nuevo_oh'])
            )
            producto_model.insertar(datos)
            return redirect(url_for('producto.index'))
        except Exception as e:
            print("Error al insertar producto:", e)

    productos_lista = producto_model.obtener_todos()
    return render_template('Productos.html', productos=productos_lista)