import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os
import tempfile
from flask import session, url_for
import warnings
warnings.filterwarnings('ignore')

class ProphetPredictor:
    """Clase para generar predicciones usando Prophet"""
    
    @staticmethod
    def predecir_producto(producto, fecha_objetivo):
        """
        Genera predicción para un producto específico en una fecha objetivo
        """
        try:
            # Obtener datos de la sesión
            if not session.get('datos_cargados'):
                return {'success': False, 'error': 'No hay datos cargados en la sesión'}
            
            df_json = session.get('df_semanal')
            if not df_json:
                return {'success': False, 'error': 'Datos no encontrados en la sesión'}
            
            # Cargar DataFrame desde JSON
            df_completo = pd.read_json(df_json)
            df_completo['fecha'] = pd.to_datetime(df_completo['fecha'])
            
            # Filtrar datos del producto específico
            df_producto = df_completo[df_completo['producto'] == producto].copy()
            
            if len(df_producto) < 20:
                return {
                    'success': False, 
                    'error': f'Producto {producto} no tiene suficientes datos históricos (mínimo 20 semanas)'
                }
            
            # Preparar datos para Prophet
            df_prophet = df_producto[['fecha', 'cantidad']].copy()
            df_prophet = df_prophet.rename(columns={'fecha': 'ds', 'cantidad': 'y'})
            df_prophet = df_prophet.sort_values('ds')
            
            # Crear y entrenar modelo Prophet
            modelo = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
                interval_width=0.8  # 80% de intervalo de confianza
            )
            
            modelo.fit(df_prophet)
            
            # Crear fechas futuras hasta la fecha objetivo
            fecha_obj = pd.to_datetime(fecha_objetivo)
            last_date = df_prophet['ds'].max()
            
            if fecha_obj <= last_date:
                return {
                    'success': False, 
                    'error': 'La fecha debe ser posterior a los datos históricos'
                }
            
            # Generar predicciones
            future = modelo.make_future_dataframe(periods=52, freq='W-MON')  # 52 semanas futuras
            forecast = modelo.predict(future)
            
            # Encontrar predicción para la fecha específica
            prediccion_fecha = ProphetPredictor._encontrar_prediccion_fecha(forecast, fecha_obj)
            
            if prediccion_fecha is None:
                return {
                    'success': False, 
                    'error': 'No se pudo generar predicción para la fecha solicitada'
                }
            
            # Generar gráfico
            grafico_url = ProphetPredictor._generar_grafico(modelo, forecast, df_prophet, producto, fecha_obj, prediccion_fecha)
            
            return {
                'success': True,
                'prediccion': int(round(prediccion_fecha['yhat'])),
                'confianza': {
                    'lower': int(round(prediccion_fecha['yhat_lower'])),
                    'upper': int(round(prediccion_fecha['yhat_upper']))
                },
                'fecha_prediccion': fecha_objetivo,
                'producto': producto,
                'grafico_url': grafico_url
            }
            
        except Exception as e:
            return {
                'success': False, 
                'error': f'Error en la predicción: {str(e)}'
            }
    
    @staticmethod
    def _encontrar_prediccion_fecha(forecast, fecha_objetivo):
        """Encuentra la predicción más cercana a la fecha objetivo"""
        # Convertir fecha objetivo al lunes de esa semana
        fecha_lunes = fecha_objetivo - timedelta(days=fecha_objetivo.weekday())
        
        # Buscar la predicción más cercana
        forecast['diff'] = abs((forecast['ds'] - fecha_lunes).dt.days)
        idx_cercano = forecast['diff'].idxmin()
        
        if forecast.loc[idx_cercano, 'diff'] <= 6:  # Dentro de la misma semana
            return forecast.loc[idx_cercano]
        
        return None
    
    @staticmethod
    def _generar_grafico(modelo, forecast, df_historico, producto, fecha_objetivo, prediccion_fecha):
        """Genera gráfico de Prophet y lo guarda como imagen"""
        try:
            # Configurar matplotlib para no usar GUI
            plt.switch_backend('Agg')
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Plotear datos históricos
            ax.plot(df_historico['ds'], df_historico['y'], 'ko', markersize=3, label='Datos históricos')
            
            # Plotear predicción
            forecast_future = forecast[forecast['ds'] > df_historico['ds'].max()]
            ax.plot(forecast_future['ds'], forecast_future['yhat'], 'b-', linewidth=2, label='Predicción')
            
            # Plotear intervalo de confianza
            ax.fill_between(forecast_future['ds'], 
                          forecast_future['yhat_lower'], 
                          forecast_future['yhat_upper'], 
                          alpha=0.3, color='lightblue', label='Intervalo de confianza (80%)')
            
            # Marcar punto específico de predicción
            ax.plot(prediccion_fecha['ds'], prediccion_fecha['yhat'], 'ro', markersize=8, 
                   label=f'Predicción objetivo: {int(round(prediccion_fecha["yhat"]))} unidades')
            
            # Configurar gráfico
            ax.set_title(f'Predicción de Demanda - {producto}', fontsize=14, fontweight='bold')
            ax.set_xlabel('Fecha', fontsize=12)
            ax.set_ylabel('Cantidad (unidades)', fontsize=12)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Formatear eje X
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            plt.xticks(rotation=45)
            
            # Ajustar layout
            plt.tight_layout()
            
            # Guardar imagen
            filename = f'prophet_{hash(producto + str(fecha_objetivo))}.png'
            filepath = os.path.join('app', 'static', 'temp_plots', filename)
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            # Retornar URL relativa
            return f'/static/temp_plots/{filename}'
            
        except Exception as e:
            print(f"Error generando gráfico: {e}")
            return None