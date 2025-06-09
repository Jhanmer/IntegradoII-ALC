# ...código existente...
from flask import render_template, Blueprint

main_bp = Blueprint('main', __name__)

# ...otras rutas...

@main_bp.route('/predecir-stock')
def predecir_stock():
    return render_template('predecir_stock.html')
# ...código existente...