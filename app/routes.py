# app/routes.py

from app.controllers.producto import producto as producto_bp

def register_routes(app):
    """
    Registra todos los Blueprints de la aplicación.
    """
    app.register_blueprint(producto_bp)
