from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_required, current_user
from app.db import get_db
from functools import wraps
from datetime import datetime, timedelta

pedido_bp = Blueprint('pedido', __name__, url_prefix='/pedidos')

# Decorador de roles permitidos
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('main.iniciar_sesion', next=request.url))
            user_role = current_user.rol.lower() if hasattr(current_user, 'rol') and current_user.rol else ''
            if user_role not in [r.lower() for r in allowed_roles]:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@pedido_bp.route('/', methods=['GET', 'POST'])
@role_required(['administrador','supervisor'])
@login_required
def index():
    db = get_db()
    cursor = db.cursor()

    # ----------------------
    # POST: Registrar pedido
    # ----------------------
    if request.method == 'POST':
        try:
            producto_id = int(request.form['producto_id'])
            cantidad = int(request.form['quantity'])

            # Obtener ambos stocks
            cursor.execute('SELECT oh_disponible, nuevo_oh FROM productos WHERE id = %s', (producto_id,))
            stock = cursor.fetchone()

            if stock:
                oh = stock[0] or 0
                nuevo = stock[1] or 0
                total_stock = oh + nuevo

                if total_stock >= cantidad:
                    # Insertar el pedido
                    cursor.execute(
                        'INSERT INTO pedidos (supervisor_id, producto_id, cantidad) VALUES (%s, %s, %s)',
                        (current_user.CodUsu, producto_id, cantidad)
                    )

                    # Descontar SOLO del nuevo_oh
                    cursor.execute(
                        'UPDATE productos SET nuevo_oh = nuevo_oh - %s WHERE id = %s',
                        (cantidad, producto_id)
                    )

                    db.commit()
                    flash('✅ Pedido registrado correctamente.', 'success')
                else:
                    flash('⚠️ Stock insuficiente (disponible + nuevo ingreso).', 'danger')
            else:
                flash('❌ Producto no encontrado.', 'danger')

        except Exception as e:
            db.rollback()
            flash(f'❌ Error al registrar el pedido: {e}', 'danger')

        return redirect(url_for('pedido.index'))

    # ----------------------
    # GET: Mostrar pedidos
    # ----------------------
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')

    filtros = ""
    params = []

    if desde:
        filtros += " AND p.fecha >= %s"
        params.append(desde)

    if hasta:
        try:
            hasta_dt = datetime.strptime(hasta, '%Y-%m-%d') + timedelta(days=1)
            filtros += " AND p.fecha < %s"
            params.append(hasta_dt.strftime('%Y-%m-%d'))
        except ValueError:
            flash('⚠️ Formato de fecha inválido.', 'warning')

    # Productos activos
    cursor.execute('SELECT id, descripcion FROM productos WHERE estado = TRUE ORDER BY descripcion')
    productos = cursor.fetchall()

    # Pedidos
    cursor.execute(f'''
        SELECT p.id, u.nombre, pr.descripcion, p.cantidad, p.fecha
        FROM pedidos p
        JOIN usuario u ON p.supervisor_id = u.CodUsu
        JOIN productos pr ON p.producto_id = pr.id
        WHERE 1=1 {filtros}
        ORDER BY p.fecha DESC
    ''', tuple(params))
    pedidos_raw = cursor.fetchall()

    pedidos = []
    for row in pedidos_raw:
        id, nombre, producto, cantidad, fecha = row
        if isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            except:
                fecha = datetime.now()
        pedidos.append((id, nombre, producto, cantidad, fecha))

    # Dashboard
    cursor.execute('SELECT COUNT(*), COALESCE(SUM(cantidad), 0) FROM pedidos')
    total_pedidos, total_unidades = cursor.fetchone()

    cursor.execute('''
        SELECT pr.descripcion, SUM(p.cantidad)
        FROM pedidos p
        JOIN productos pr ON p.producto_id = pr.id
        GROUP BY pr.descripcion
        ORDER BY SUM(p.cantidad) DESC
        LIMIT 5
    ''')
    top_productos = cursor.fetchall()

    return render_template(
        'Pedidos.html',
        productos=productos,
        pedidos=pedidos,
        total_pedidos=total_pedidos,
        total_unidades=total_unidades,
        top_productos=top_productos
    )


# -----------------------------
# API: Stock en tiempo real
# -----------------------------
@pedido_bp.route('/api/stock/<int:producto_id>')
@login_required
def api_stock(producto_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT oh_disponible, nuevo_oh FROM productos WHERE id = %s', (producto_id,))
    stock = cursor.fetchone()

    total = (stock[0] or 0) + (stock[1] or 0) if stock else 0
    return jsonify({'stock': total})


# -----------------------------
# AJAX: Registrar pedido
# -----------------------------
@pedido_bp.route('/ajax_registrar', methods=['POST'])
@login_required
def ajax_registrar():
    db = get_db()
    cursor = db.cursor()
    try:
        producto_id = int(request.form['producto_id'])
        cantidad = int(request.form['quantity'])

        cursor.execute('SELECT oh_disponible, nuevo_oh FROM productos WHERE id = %s', (producto_id,))
        stock = cursor.fetchone()

        if not stock:
            return jsonify({'success': False, 'message': 'Producto no encontrado.'})

        total_stock = (stock[0] or 0) + (stock[1] or 0)
        if total_stock < cantidad:
            return jsonify({'success': False, 'message': 'Stock insuficiente para este producto.'})

        cursor.execute(
            'INSERT INTO pedidos (supervisor_id, producto_id, cantidad) VALUES (%s, %s, %s)',
            (current_user.CodUsu, producto_id, cantidad)
        )

        cursor.execute(
            'UPDATE productos SET nuevo_oh = nuevo_oh - %s WHERE id = %s',
            (cantidad, producto_id)
        )

        db.commit()
        return jsonify({'success': True, 'message': '✅ Pedido registrado correctamente.'})

    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': f'❌ Error: {str(e)}'})