# app/controllers/main.py
from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
import pandas as pd
import os
from werkzeug.utils import secure_filename
from app.utils.excel_processor import ExcelProcessor
from app.utils.prophet_predictor import ProphetPredictor

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/pedidos') # Nueva ruta para Pedidos
def pedidos():
    return render_template('Pedidos.html')

# ========== SISTEMA DE PREDICCIONES ==========

@main_bp.route('/predicciones')
def predicciones_dashboard():
    """Dashboard principal del sistema de predicciones"""
    return render_template('dashboard_predicciones.html')

@main_bp.route('/predicciones/cargar-datos')
def cargar_datos():
    """Página para cargar archivo Excel"""
    return render_template('cargar_datos.html')

@main_bp.route('/predecir-stock')
def predecir_stock():
    """Página de predicción - template actual"""
    if not session.get('datos_cargados'):
        return redirect(url_for('main.predicciones_dashboard'))
    
    return render_template('predecir_stock.html')

@main_bp.route('/api/cargar-excel', methods=['POST'])
def cargar_excel():
    """API endpoint para procesar archivo Excel"""
    # Verificar archivo
    if 'archivo' not in request.files:
        return jsonify({'success': False, 'error': 'No se seleccionó ningún archivo'})
    
    archivo = request.files['archivo']
    
    if archivo.filename == '':
        return jsonify({'success': False, 'error': 'No se seleccionó ningún archivo'})
    
    if not archivo.filename.lower().endswith('.xlsx'):
        return jsonify({'success': False, 'error': 'Solo se permiten archivos .xlsx'})
    
    # Procesar archivo usando la clase especializada
    resultado = ExcelProcessor.procesar_archivo(archivo)
    
    return jsonify(resultado)

@main_bp.route('/api/obtener-productos')
def obtener_productos():
    """API para obtener lista de productos disponibles"""
    if not session.get('datos_cargados'):
        return jsonify({'success': False, 'error': 'No hay datos cargados'})
    
    productos = session.get('productos_list', [])
    return jsonify({'success': True, 'productos': productos})

@main_bp.route('/api/predecir-prophet', methods=['POST'])
def predecir_prophet():
    """API endpoint para generar predicción con Prophet"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No se enviaron datos'})
        
        producto = data.get('producto')
        fecha = data.get('fecha')
        
        if not producto or not fecha:
            return jsonify({'success': False, 'error': 'Producto y fecha son requeridos'})
        
        # Verificar que hay datos cargados
        if not session.get('datos_cargados'):
            return jsonify({'success': False, 'error': 'No hay datos cargados. Carga un archivo Excel primero.'})
        
        # Generar predicción usando Prophet
        resultado = ProphetPredictor.predecir_producto(producto, fecha)
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Error en el servidor: {str(e)}'
        })