# app/controllers/usuario.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.usuario import Usuario # Necesitamos la clase Usuario para crear objetos
from app.config import get_db_connection # Necesitamos tu función de conexión

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
@login_required
def list_users():
    if current_user.rol != 'administrador':
        flash('Solo los administradores pueden gestionar usuarios.', 'warning')
        return redirect(url_for('main.dashboard_index'))

    conn = None
    cur = None
    users = []
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT CodUsu, nombre, rol, login, password, estado FROM usuario ORDER BY CodUsu")
            users_data = cur.fetchall()
            for user_d in users_data:
                # Crear instancias de Usuario con los datos leídos de la BD
                users.append(Usuario(CodUsu=user_d[0], nombre=user_d[1], rol=user_d[2],
                                     login=user_d[3], password=user_d[4], estado=user_d[5]))
        else:
            flash('Error al conectar con la base de datos para obtener usuarios.', 'danger')
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        flash('Ocurrió un error inesperado al obtener usuarios.', 'danger')
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return render_template('usuarios.html', users=users)
