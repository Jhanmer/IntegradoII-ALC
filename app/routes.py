# app/routes.py

# Importa la instancia del Blueprint desde tu controlador
from app.controllers.producto import producto as producto_bp # Renombrado para evitar conflicto de nombres

def register_routes(app):
    """
    Registra todos los Blueprints de la aplicación.
    """
    app.register_blueprint(producto_bp)
    # Si tuvieras más controladores/blueprints, los registrarías aquí:
    # from app.controllers.otro_modulo import otro_bp
    # app.register_blueprint(otro_bp)