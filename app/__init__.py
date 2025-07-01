# app/__init__.py
from flask import Flask, redirect, url_for

def create_app():
    app = Flask(__name__)

    # --- Configuración de la aplicación ---
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SECRET_KEY'] = 'clave-secreta-para-sesiones-123'  # ← Agregar esta línea

    # --- ---
    from app.controllers.producto import producto_bp
    app.register_blueprint(producto_bp)

    from app.controllers.main import main_bp
    app.register_blueprint(main_bp)

    # <<-- -->>
    from app.controllers.pedido import pedido_bp
    app.register_blueprint(pedido_bp)
    # <<-- -->>

    # --- Rutas Globales o de Redirección ---
    @app.route('/')
    def root_redirect():
        return redirect(url_for('main.index'))

    return app