from flask import Flask, redirect, url_for, render_template, abort
from flask_login import LoginManager
from app.config import get_db_connection
from app.models.gestion import Usuario  # Usamos el nuevo modelo gestion.py

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.secret_key = '12345'  # Cambiar por una clave segura en producción
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # Inicializar LoginManager
    login_manager.init_app(app)
    login_manager.login_view = 'main.iniciar_sesion'
    login_manager.login_message_category = 'info'

    # Registro de Blueprints
    from app.controllers.main import main_bp
    app.register_blueprint(main_bp)

    from app.controllers.gestion import gestion_bp 
    app.register_blueprint(gestion_bp, url_prefix='/usuarios')

    from app.controllers.producto import producto_bp
    app.register_blueprint(producto_bp)

    from app.controllers.pedido import pedido_bp
    app.register_blueprint(pedido_bp)

    from app.controllers.panel import panel_bp
    app.register_blueprint(panel_bp)

    from app.controllers.listpedidos import listpedidos_bp
    app.register_blueprint(listpedidos_bp)
    
    # Manejo de errores personalizados
    @app.errorhandler(403)
    def acceso_prohibido(e):
        return render_template('403.html'), 403

    return app

# Carga de usuario desde la base de datos para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT CodUsu, nombre, rol, login, password, estado
                FROM usuario WHERE CodUsu = %s
            """, (user_id,))
            user_data = cur.fetchone()
            if user_data:
                return Usuario(
                    CodUsu=user_data[0],
                    nombre=user_data[1],
                    rol=user_data[2],
                    login=user_data[3],
                    password=user_data[4],
                    estado=user_data[5]
                )
    except Exception as e:
        print(f"Error al cargar usuario por ID: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return None