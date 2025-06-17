# app/__init__.py
from flask import Flask, redirect, url_for
from flask_login import LoginManager, UserMixin 
from app.config import get_db_connection 

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.secret_key = '12345'  # Clave secreta para sesiones y protección CSRF
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # --- Inicializar Flask-Login con la aplicación ---
    login_manager.init_app(app) # Asocia LoginManager con tu instancia de Flask
    login_manager.login_view = 'main.iniciar_sesion' # Ruta a la página de login si se requiere autenticación
    login_manager.login_message_category = 'info' # Categoría para mensajes flash de login_required

    # --- Importar y registrar los Blueprints ---
    # Es importante que estos se importen DESPUÉS de que login_manager se haya inicializado con 'app'
    from app.controllers.main import main_bp
    app.register_blueprint(main_bp)

    from app.controllers.usuario import user_bp # Asumiendo que tienes este controller
    app.register_blueprint(user_bp, url_prefix='/usuarios') # Registra el Blueprint de usuarios

    from app.controllers.producto import producto_bp # Tu blueprint de producto
    app.register_blueprint(producto_bp)

    from app.controllers.pedido import pedido_bp # Tu blueprint de pedido
    app.register_blueprint(pedido_bp)

    return app

# --- Clase User y user_loader para Flask-Login ---
# Esta clase y función son usadas por Flask-Login para manejar las sesiones de usuario.
class User(UserMixin):
    def __init__(self, id, nombre, rol, login, password, estado):
        self.id = id
        self.nombre = nombre
        self.rol = rol
        self.login = login
        self.password = password
        self.estado = estado

    def get_id(self):
        return str(self.id)

# Esta función es crucial para que Flask-Login cargue al usuario desde la sesión.
@login_manager.user_loader
def load_user(user_id):
    conn = None
    cur = None
    try:
        conn = get_db_connection() # Usa tu función para obtener la conexión a la BD
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT CodUsu, nombre, rol, login, password, estado FROM usuario WHERE CodUsu = %s", (user_id,))
            user_data = cur.fetchone()
            if user_data:
                # Crea una instancia de tu clase User simple con los datos de la BD
                return User(id=user_data[0], nombre=user_data[1], rol=user_data[2], login=user_data[3], password=user_data[4], estado=user_data[5])
            else:
                return None
    except Exception as e:
        print(f"Error al cargar usuario por ID: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()