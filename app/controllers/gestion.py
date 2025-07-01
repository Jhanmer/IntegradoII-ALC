from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from app.config import get_db_connection
import random
import string

gestion_bp = Blueprint('gestion', __name__)

# Decorador para restringir acceso por roles
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('main.iniciar_sesion', next=request.url))
            if current_user.rol.lower() not in [r.lower() for r in allowed_roles]:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Vista principal de gestión
@gestion_bp.route('/')
@login_required
@role_required(['Administrador'])
def index():
    return render_template('usuarios.html', title='Gestión de Usuarios')

# Listar usuarios para la tabla
@gestion_bp.route('/listar', methods=['GET'])
@login_required
@role_required(['Administrador'])
def listar_usuarios():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT CodUsu, nombre, login, rol, estado FROM usuario ORDER BY CodUsu ASC")
        usuarios = cur.fetchall()
        data = [
            {
                "CodUsu": u[0],
                "nombre": u[1],
                "login": u[2],
                "rol": u[3],
                "estado": u[4]
            } for u in usuarios
        ]
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()

# Registrar nuevo usuario
@gestion_bp.route('/registrar', methods=['POST'])
@login_required
@role_required(['Administrador'])
def registrar_usuario():
    data = request.json
    nombre = data.get('nombre')
    login = data.get('login')
    password = data.get('password')
    rol = data.get('rol')
    estado = data.get('estado')

    if not all([nombre, login, password, rol, estado]):
        return jsonify({'error': 'Faltan datos'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO usuario (nombre, login, password, rol, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, login, password, rol, estado))
        conn.commit()
        return jsonify({'mensaje': 'Usuario registrado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()

# Cambiar contraseña
@gestion_bp.route('/cambiar_password', methods=['POST'])
@login_required
@role_required(['Administrador'])
def cambiar_password():
    data = request.json
    user_id = data.get('id')
    nueva_password = data.get('nuevaPassword')

    if not user_id or not nueva_password:
        return jsonify({'error': 'Datos incompletos'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE usuario SET password = %s WHERE CodUsu = %s", (nueva_password, user_id))
        conn.commit()
        return jsonify({'mensaje': 'Contraseña actualizada correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()

# Cambiar estado activo/inactivo
@gestion_bp.route('/cambiar_estado', methods=['POST'])
@login_required
@role_required(['Administrador'])
def cambiar_estado():
    data = request.json
    user_id = data.get('id')
    nuevo_estado = data.get('estado')

    if not user_id or not nuevo_estado:
        return jsonify({'error': 'Datos incompletos'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE usuario SET estado = %s WHERE CodUsu = %s", (nuevo_estado, user_id))
        conn.commit()
        return jsonify({'mensaje': 'Estado actualizado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()

# Generar contraseña aleatoria
@gestion_bp.route('/generar_password', methods=['GET'])
@login_required
@role_required(['Administrador'])
def generar_password():
    password = ''.join(random.choices(string.ascii_letters, k=5))
    return jsonify({'password': password})