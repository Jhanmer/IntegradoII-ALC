# app/controllers/main.py
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('home.html') #

@main_bp.route('/pedidos') # Nueva ruta para Pedidos
def pedidos():
    return render_template('Pedidos.html')

@main_bp.route('/predecir-stock')
def predecir_stock():
    return render_template('predecir_stock.html')

@main_bp.route('/iniciar-sesion') 
def iniciar_sesion():
    return render_template('iniciosession.html')

@main_bp.route('/dashboard') 
def dashboard_index():
    return render_template('index.html')

@main_bp.route('/gestion-pedidos') 
def gestion_pedidos():
    return render_template('GPedidos.html')

@main_bp.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')