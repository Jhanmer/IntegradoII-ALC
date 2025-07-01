from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from functools import wraps

user_bp = Blueprint('user', __name__)

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
@user_bp.route('/')
@login_required
@role_required(['administrador'])
def index():
    return render_template('usuarios.html', title='Gestión de Usuarios')