from flask import Blueprint, render_template
from flask_login import login_required
from app.db import get_db
from datetime import datetime, timedelta

panel_bp = Blueprint('panel', __name__)

@panel_bp.route('/panel')
@login_required
def panel():
    db = get_db()
    cursor = db.cursor()

    # Pedidos actuales y semana pasada
    cursor.execute('SELECT COUNT(*) FROM pedidos')
    total_pedidos = cursor.fetchone()[0]

    hoy = datetime.now()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio_semana_pasada = inicio_semana - timedelta(weeks=1)
    fin_semana_pasada = inicio_semana - timedelta(seconds=1)

    cursor.execute('''SELECT COUNT(*) FROM pedidos WHERE fecha BETWEEN %s AND %s''', (inicio_semana_pasada, fin_semana_pasada))
    pedidos_semana_pasada = cursor.fetchone()[0]

    porcentaje_cambio_pedidos = 0
    if pedidos_semana_pasada > 0:
        porcentaje_cambio_pedidos = round((total_pedidos - pedidos_semana_pasada) / pedidos_semana_pasada * 100, 2)

    # Usuarios
    cursor.execute('SELECT COUNT(*) FROM usuario')
    total_usuarios = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM usuario WHERE estado = %s', ('activo',))
    usuarios_activos = cursor.fetchone()[0]

    porcentaje_cambio_usuarios = 0
    if usuarios_activos > 0:
        porcentaje_cambio_usuarios = round((total_usuarios - usuarios_activos) / usuarios_activos * 100, 2)

    # Predicciones simuladas
    predicciones = 3

    # Stock
    cursor.execute('SELECT COUNT(*) FROM productos WHERE oh_disponible = 0')
    sin_stock = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM productos WHERE oh_disponible BETWEEN 1 AND 5')
    pre_quiebre = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM productos WHERE oh_disponible < 0')
    quiebre = cursor.fetchone()[0]

    # Top 5 productos más pedidos
    cursor.execute('''
        SELECT pr.descripcion, SUM(p.cantidad) AS total
        FROM pedidos p
        JOIN productos pr ON p.producto_id = pr.id
        GROUP BY pr.descripcion
        ORDER BY total DESC
        LIMIT 5
    ''')
    top_productos = cursor.fetchall()

    # Últimos productos registrados
    cursor.execute('''
        SELECT pr.descripcion, pr.fecha_creacion, pr.estado, u.nombre
        FROM productos pr
        LEFT JOIN usuario u ON pr.marca_id = u.CodUsu
        ORDER BY pr.fecha_creacion DESC
        LIMIT 10
    ''')
    productos = cursor.fetchall()

    return render_template('index.html',
        total_pedidos=total_pedidos,
        porcentaje_cambio_pedidos=porcentaje_cambio_pedidos,
        total_usuarios=total_usuarios,
        porcentaje_cambio_usuarios=porcentaje_cambio_usuarios,
        predicciones=predicciones,
        sin_stock=sin_stock,
        pre_quiebre=pre_quiebre,
        quiebre=quiebre,
        top_productos=top_productos,
        productos=productos
    )