# app/controllers/pedido.py
from flask import Blueprint, render_template, request, redirect, url_for

# Asegúrate de que el Blueprint se llame 'pedido'
pedido_bp = Blueprint('pedido', __name__, url_prefix='/pedidos')

@pedido_bp.route('/')
def index():
    return render_template('Pedidos.html') # Asegúrate que Pedidos.html exista en app/templates/