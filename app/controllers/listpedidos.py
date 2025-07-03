from flask import Blueprint, render_template
from flask_login import login_required
from app.db import get_db

listpedidos_bp = Blueprint('listpedidos', __name__, url_prefix='/gestion-pedidos')

@listpedidos_bp.route('/')
@login_required
def listar_pedidos():
    db = get_db()
    cursor = db.cursor()

    # Agrupar por producto: última fecha, último supervisor, suma de cantidades
    cursor.execute('''
        SELECT 
            pr.descripcion AS producto,
            SUM(p.cantidad) AS total_cantidad,
            MAX(p.fecha) AS ultima_fecha,
            (
                SELECT u.nombre
                FROM pedidos p2
                JOIN usuario u ON p2.supervisor_id = u.CodUsu
                WHERE p2.producto_id = p.producto_id
                ORDER BY p2.fecha DESC
                LIMIT 1
            ) AS supervisor,
            pr.oh_disponible,
            pr.nuevo_oh
        FROM pedidos p
        JOIN productos pr ON p.producto_id = pr.id
        GROUP BY pr.descripcion, pr.oh_disponible, pr.nuevo_oh, p.producto_id
        ORDER BY ultima_fecha DESC
    ''')
    registros = cursor.fetchall()

    pedidos = []
    for row in registros:
        producto, total_cantidad, fecha, supervisor, oh, nuevo = row
        stock_total = (oh or 0) + (nuevo or 0)

        if stock_total <= 0:
            estado = 'Quiebre'
            color = 'danger'
        elif stock_total <= 10:
            estado = 'Pre-quiebre'
            color = 'warning'
        elif stock_total <= 30:
            estado = 'Bajo'
            color = 'info'
        else:
            estado = 'Suficiente'
            color = 'success'

        pedidos.append({
            'producto': producto,
            'cantidad': total_cantidad,
            'fecha': fecha,
            'supervisor': supervisor,
            'stock_total': stock_total,
            'estado': estado,
            'color': color
        })

    return render_template('GPedidos.html', pedidos=pedidos)