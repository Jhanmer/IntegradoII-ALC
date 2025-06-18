# app/routes/producto.py

from flask import Blueprint, render_template, request, redirect, url_for
from app.models import producto as producto_model 
from app.config import get_db_connection
from flask import flash
from flask import Flask
from flask_login import login_required, current_user
from functools import wraps

app = Flask(__name__)
app.secret_key = '12345'
producto_bp = Blueprint('producto', __name__, url_prefix='/productos')

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('main.iniciar_sesion', next=request.url))

            user_role = current_user.rol.lower() if hasattr(current_user, 'rol') and current_user.rol else ''

            if user_role not in [role.lower() for role in allowed_roles]:
                flash('No tienes permiso para acceder a esta sección.', 'danger')
                # Redirige a la página principal de tu aplicación si no tiene acceso
                return redirect(url_for('main.index')) # O a 'main.dashboard_index' si es más apropiado
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@producto_bp.route('/', methods=['GET', 'POST'])
@login_required
@role_required(['mercader'])
def index():
    if request.method == 'POST':
        try:
            datos = (
                request.form['descripcion'],
                request.form['sku'],
                int(request.form['marca']),  
                int(request.form['proveedor']),       
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
    marcas_lista = producto_model.obtener_marcas()
    proveedores_lista = producto_model.obtener_proveedores()
    return render_template(
    'Productos.html',
    productos=productos_lista,
    marcas=marcas_lista,
    proveedores=proveedores_lista
)

@producto_bp.route('/agregar_marca', methods=['POST'])
def agregar_marca():
    nombre = request.form['nueva_marca']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM marcas WHERE LOWER(nombre) = LOWER(%s)", (nombre,))
    existe = cur.fetchone()
    if not existe:
        cur.execute("INSERT INTO marcas (nombre) VALUES (%s)", (nombre,))
        conn.commit()
        flash("Marca agregada exitosamente.", "success")
    else:
        flash("La marca ya existe.", "warning")
    cur.close()
    conn.close()
    return redirect(url_for('producto.index'))

@producto_bp.route('/agregar_proveedor', methods=['POST'])
def agregar_proveedor():
    nombre = request.form.get('nuevo_proveedor')
    if nombre:
        producto_model.agregar_proveedor(nombre)
    return redirect(url_for('producto.index'))
