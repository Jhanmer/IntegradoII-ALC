from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.db import get_db
from datetime import datetime

pedido_bp = Blueprint('pedido', __name__, url_prefix='/pedidos')

@pedido_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        try:
            producto_id = int(request.form['producto_id'])
            cantidad = int(request.form['quantity'])

            cursor.execute('SELECT oh_disponible FROM productos WHERE id = %s', (producto_id,))
            stock = cursor.fetchone()

            if stock and stock[0] >= cantidad:
                cursor.execute(
                    'INSERT INTO pedidos (supervisor_id, producto_id, cantidad) VALUES (%s, %s, %s)',
                    (current_user.id, producto_id, cantidad)
                )
                cursor.execute(
                    'UPDATE productos SET oh_disponible = oh_disponible - %s WHERE id = %s',
                    (cantidad, producto_id)
                )
                db.commit()
                flash('✅ Pedido registrado correctamente.', 'success')
            else:
                flash('⚠️ Stock insuficiente para este producto.', 'danger')

        except Exception as e:
            db.rollback()
            flash(f'❌ Error: {e}', 'danger')

        return redirect(url_for('pedido.index'))

    # --- Filtros de búsqueda ---
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')

    filtros = ""
    params = []

    if desde:
        filtros += " AND p.fecha >= %s"
        params.append(desde)
    if hasta:
        filtros += " AND p.fecha <= %s"
        params.append(hasta)

    # --- Productos activos ---
    cursor.execute('SELECT id, descripcion FROM productos WHERE estado = TRUE ORDER BY descripcion')
    productos = cursor.fetchall()

    # --- Historial filtrado ---
    cursor.execute(f'''
        SELECT p.id, u.nombre, pr.descripcion, p.cantidad, p.fecha
        FROM pedidos p
        JOIN usuario u ON p.supervisor_id = u.CodUsu
        JOIN productos pr ON p.producto_id = pr.id
        WHERE 1=1 {filtros}
        ORDER BY p.fecha DESC
    ''', tuple(params))
    pedidos = cursor.fetchall()

    # --- Mini resumen para dashboard ---
    cursor.execute('SELECT COUNT(*), COALESCE(SUM(cantidad), 0) FROM pedidos')
    total_pedidos, total_unidades = cursor.fetchone()

    cursor.execute('''
        SELECT pr.descripcion, SUM(p.cantidad) AS total
        FROM pedidos p
        JOIN productos pr ON p.producto_id = pr.id
        GROUP BY pr.descripcion
        ORDER BY total DESC
        LIMIT 5
    ''')
    top_productos = cursor.fetchall()

    return render_template('Pedidos.html',
                           productos=productos,
                           pedidos=pedidos,
                           total_pedidos=total_pedidos,
                           total_unidades=total_unidades,
                           top_productos=top_productos)

@pedido_bp.route('/api/stock/<int:producto_id>')
@login_required
def api_stock(producto_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT oh_disponible FROM productos WHERE id = %s', (producto_id,))
    stock = cursor.fetchone()
    return jsonify({'stock': stock[0] if stock else 0})
