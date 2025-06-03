# app/controllers/main.py
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/pedidos') # Nueva ruta para Pedidos
def pedidos():
    return render_template('Pedidos.html')