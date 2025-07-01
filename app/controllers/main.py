from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app.models.usuario import Usuario
from app.config import get_db_connection
from functools import wraps
from urllib.parse import urlparse as url_parse

main_bp = Blueprint('main', __name__)

# Decorador para verificar roles
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('main.iniciar_sesion', next=request.url))

            user_role = current_user.rol.lower() if hasattr(current_user, 'rol') and current_user.rol else ''
            if user_role not in [role.lower() for role in allowed_roles]:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@main_bp.route('/')
def index():
    return render_template('home.html')

@main_bp.route('/pedidos')
@login_required
@role_required(['administrador', 'supervisor', 'almacen'])
def pedidos():
    return render_template('Pedidos.html')

@main_bp.route('/dashboard')
@login_required
@role_required(['administrador', 'supervisor', 'mercader', 'almacen'])
def dashboard_index():
    return redirect(url_for('panel.panel'))

@main_bp.route('/predecir-stock')
@login_required
@role_required(['administrador', 'supervisor', 'almacen'])
def predecir_stock():
    return render_template('predecir_stock.html')

@main_bp.route('/gestion-pedidos')
@login_required
@role_required(['administrador', 'supervisor', 'almacen'])
def gestion_pedidos():
    return render_template('GPedidos.html')

@main_bp.route('/usuarios')
@login_required
@role_required(['administrador'])
def usuarios():
    return render_template('usuarios.html')

@main_bp.route('/iniciar-sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_index'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember-me') else False

        conn = None
        cur = None
        user = None

        try:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                cur.execute("SELECT CodUsu, nombre, rol, login, password, estado FROM usuario WHERE login = %s", (email,))
                user_data = cur.fetchone()

                if user_data:
                    user = Usuario(
                        CodUsu=user_data[0],
                        nombre=user_data[1],
                        rol=user_data[2],
                        login=user_data[3],
                        password=user_data[4],
                        estado=user_data[5]
                    )

                    if user.estado.lower() != 'activo':
                        flash('Tu cuenta está inactiva. Contacta al administrador.', 'danger')
                        return render_template('iniciosession.html')

                    if user.check_password(password):
                        login_user(user, remember=remember)
                        flash(f'¡Bienvenido, {user.nombre}!', 'success')
                        next_page = request.args.get('next')

                        if next_page and url_parse(next_page).netloc != '' and \
                        url_parse(next_page).netloc != request.host_url.split('//')[-1].split(':')[0]:
                            flash('Redirección a URL externa bloqueada.', 'danger')
                            return redirect(url_for('main.dashboard_index'))

                        return redirect(next_page or url_for('main.dashboard_index'))
                    else:
                        flash('Inicio de sesión fallido. Por favor, verifica tu correo y contraseña.', 'danger')
                else:
                    flash('Inicio de sesión fallido. Por favor, verifica tu correo y contraseña.', 'danger')
            else:
                flash('Error al conectar con la base de datos.', 'danger')
        except Exception as e:
            print(f"Error durante el inicio de sesión: {e}")
            flash('Ocurrió un error inesperado durante el inicio de sesión.', 'danger')
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

        return render_template('iniciosession.html')

    return render_template('iniciosession.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('main.index'))