from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from functools import wraps
from app.models import producto as producto_model
from app.config import get_db_connection

producto_bp = Blueprint('producto', __name__, url_prefix='/productos')

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

# Vista principal: productos y formularios
@producto_bp.route('/', methods=['GET', 'POST'])
@login_required
@role_required(['administrador','mercader','supervisor'])
def index():
    if request.method == 'POST':
        try:
            descripcion = request.form['descripcion'].strip()

            if producto_model.descripcion_existe(descripcion):
                flash("Ya existe un producto con esa descripción.", "warning")
                return redirect(url_for('producto.index', duplicada=1, valor=descripcion))

            datos = (
                descripcion,
                request.form['sku'].strip(),
                int(request.form['marca']),
                int(request.form['proveedor']),
                request.form['division'],
                request.form['estado'].lower() == 'activo',
                int(request.form['oh_disponible']),
                int(request.form['nuevo_oh'])
            )

            producto_model.insertar_o_actualizar(datos)
            flash("Producto registrado correctamente.", "success")
            return redirect(url_for('producto.index', valida=1, valor=descripcion))

        except Exception as e:
            import traceback
            print("🛑 ERROR en controlador /producto:", repr(e))
            traceback.print_exc()
            flash("Ocurrió un error al procesar el producto.", "danger")
            return redirect(url_for('producto.index'))

    # Vista GET o después de redirect
    productos_lista = producto_model.obtener_todos()
    marcas_lista = producto_model.obtener_marcas()
    proveedores_lista = producto_model.obtener_proveedores()
    descripciones_lista = producto_model.obtener_descripciones()

    return render_template(
        'Productos.html',
        productos=productos_lista,
        marcas=marcas_lista,
        proveedores=proveedores_lista,
        productos_descripciones=descripciones_lista
    )


# Actualizar stock (por selección de producto existente)
@producto_bp.route('/actualizar', methods=['POST'])
@login_required
@role_required(['administrador','mercader'])
def actualizar_producto():
    try:
        sku = request.form['sku_existente']
        nuevo_oh = int(request.form['nuevo_oh_actualizar'])
        producto_model.actualizar_stock_por_sku(sku, nuevo_oh)
        flash("Stock actualizado correctamente.", "success")
    except Exception as e:
        print("Error al actualizar stock:", e)
        flash("Error al actualizar stock.", "danger")
    return redirect(url_for('producto.index'))

# Agregar nueva marca
@producto_bp.route('/agregar_marca', methods=['POST'])
@login_required
@role_required(['administrador','mercader'])
def agregar_marca():
    nombre = request.form['nueva_marca'].strip()
    
    if not nombre:
        flash("Nombre de marca inválido.", "danger")
        return redirect(url_for('producto.index'))

    try:
        # Verificar si ya existe una marca con ese nombre
        marca_existente = producto_model.obtener_marca_por_nombre(nombre)
        if marca_existente:
            flash("La marca ya existe.", "warning")
        else:
            producto_model.insertar_marca(nombre)
            flash("Marca agregada exitosamente.", "success")
    except Exception as e:
        flash(f"Error al agregar marca: {e}", "danger")

    return redirect(url_for('producto.index'))

# Agregar nuevo proveedor
@producto_bp.route('/agregar_proveedor', methods=['POST'])
@login_required
@role_required(['administrador','mercader'])
def agregar_proveedor():
    nombre = request.form.get('nuevo_proveedor', '').strip()
    if not nombre:
        flash("Nombre de proveedor inválido.", "danger")
        return redirect(url_for('producto.index'))

    try:
        # Verificar si el proveedor ya existe
        proveedor_existente = producto_model.obtener_proveedor_por_nombre(nombre)
        if proveedor_existente:
            flash("El proveedor ya existe.", "warning")
        else:
            producto_model.agregar_proveedor(nombre)
            flash("Proveedor agregado exitosamente.", "success")
    except Exception as e:
        flash(f"Error al agregar proveedor: {e}", "danger")

    return redirect(url_for('producto.index'))

@producto_bp.route('/validar_descripcion')
@login_required
def validar_descripcion():
    descripcion = request.args.get('descripcion', '').strip()
    
    if not descripcion:
        return {"valido": False, "mensaje": "Descripción vacía"}

    existe = producto_model.descripcion_existe(descripcion)
    
    return {"valido": not existe}