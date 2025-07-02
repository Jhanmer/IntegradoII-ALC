import pandas as pd
from datetime import datetime
from flask import session

class ExcelProcessor:
    """Clase para procesar archivos Excel de ventas"""
    
    @staticmethod
    def procesar_archivo(archivo):
        """
        Procesa archivo Excel y retorna resultado estructurado
        """
        try:
            # Leer Excel
            df = pd.read_excel(archivo)
            
            # Validar columnas requeridas
            columnas_requeridas = ['Fecha', 'Cantidad pedido', 'Descripción']
            columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
            
            if columnas_faltantes:
                return {
                    'success': False, 
                    'error': f'Columnas faltantes en el Excel: {", ".join(columnas_faltantes)}'
                }
            
            # Limpiar y procesar datos
            df_procesado = ExcelProcessor._limpiar_datos(df)
            
            if df_procesado is None:
                return {
                    'success': False, 
                    'error': 'Error al procesar los datos. Verifica el formato de fechas y cantidades.'
                }
            
            # Validar cantidad mínima de datos
            if len(df_procesado) < 20:
                return {
                    'success': False, 
                    'error': 'El archivo debe contener al menos 20 registros de datos históricos.'
                }
            
            # Agrupar por semanas
            df_semanal = ExcelProcessor._agrupar_por_semanas(df_procesado)
            
            # Validar productos con datos suficientes
            productos_validos = ExcelProcessor._validar_productos(df_semanal)
            
            if not productos_validos:
                return {
                    'success': False, 
                    'error': 'Ningún producto tiene suficientes datos históricos (mínimo 5 meses/20 semanas).'
                }
            
            # Obtener estadísticas
            estadisticas = ExcelProcessor._obtener_estadisticas(df_semanal, productos_validos)
            
            # Guardar en sesión
            ExcelProcessor._guardar_en_sesion(df_semanal, estadisticas)
            
            # Generar preview
            preview_html = ExcelProcessor._generar_preview_html(df_semanal.head(10))
            
            return {
                'success': True,
                **estadisticas,
                'preview': preview_html
            }
            
        except Exception as e:
            return {
                'success': False, 
                'error': f'Error al procesar el archivo: {str(e)}'
            }
    
    @staticmethod
    def _limpiar_datos(df):
        """Limpia y valida los datos del Excel"""
        try:
            # Crear copia
            df_procesado = df.copy()
            
            # Renombrar columnas
            df_procesado = df_procesado.rename(columns={
                'Fecha': 'fecha',
                'Cantidad pedido': 'cantidad',
                'Descripción': 'producto'
            })
            
            # Convertir fecha
            try:
                df_procesado['fecha'] = pd.to_datetime(df_procesado['fecha'], format='%d/%m/%Y')
            except:
                try:
                    df_procesado['fecha'] = pd.to_datetime(df_procesado['fecha'], dayfirst=True)
                except:
                    return None
            
            # Convertir cantidad a numérico
            df_procesado['cantidad'] = pd.to_numeric(df_procesado['cantidad'], errors='coerce')
            
            # Eliminar filas con datos inválidos
            df_procesado = df_procesado.dropna(subset=['fecha', 'cantidad', 'producto'])
            
            # Filtrar cantidades válidas
            df_procesado = df_procesado[df_procesado['cantidad'] > 0]
            
            # Limpiar nombres de productos
            df_procesado['producto'] = df_procesado['producto'].str.strip()
            
            return df_procesado
            
        except Exception as e:
            print(f"Error en _limpiar_datos: {e}")
            return None
    
    @staticmethod
    def _agrupar_por_semanas(df):
        """Agrupa datos diarios en semanas"""
        try:
            # Crear columna de semana (lunes como inicio)
            df['semana'] = df['fecha'].dt.to_period('W-MON')
            
            # Agrupar por semana y producto
            df_semanal = df.groupby(['semana', 'producto'])['cantidad'].sum().reset_index()
            
            # Convertir período a fecha
            df_semanal['fecha'] = df_semanal['semana'].dt.start_time
            
            # Limpiar y ordenar
            df_semanal = df_semanal.drop('semana', axis=1)
            df_semanal = df_semanal.sort_values(['fecha', 'producto'])
            
            return df_semanal
            
        except Exception as e:
            print(f"Error en _agrupar_por_semanas: {e}")
            return df
    
    @staticmethod
    def _validar_productos(df_semanal):
        """Valida que productos tengan suficientes datos"""
        productos_validos = []
        
        for producto in df_semanal['producto'].unique():
            datos_producto = df_semanal[df_semanal['producto'] == producto]
            if len(datos_producto) >= 20:  # Mínimo 20 semanas
                productos_validos.append(producto)
        
        return sorted(productos_validos)
    
    @staticmethod
    def _obtener_estadisticas(df_semanal, productos_validos):
        """Calcula estadísticas de los datos procesados"""
        return {
            'productos_count': len(productos_validos),
            'registros_count': len(df_semanal),
            'fecha_inicio': df_semanal['fecha'].min().strftime('%d/%m/%Y'),
            'fecha_fin': df_semanal['fecha'].max().strftime('%d/%m/%Y'),
            'productos_list': productos_validos
        }
    
    @staticmethod
    def _guardar_en_sesion(df_semanal, estadisticas):
        """Guarda datos procesados en la sesión Flask"""
        session['datos_cargados'] = True
        session['df_semanal'] = df_semanal.to_json(date_format='iso')
        session['productos_count'] = estadisticas['productos_count']
        session['productos_list'] = estadisticas['productos_list']
        session['registros_count'] = estadisticas['registros_count']
        session['fecha_inicio'] = estadisticas['fecha_inicio']
        session['fecha_fin'] = estadisticas['fecha_fin']
    
    @staticmethod
    def _generar_preview_html(df_sample):
        """Genera HTML para preview de datos"""
        try:
            df_display = df_sample.copy()
            df_display['fecha'] = df_display['fecha'].dt.strftime('%d/%m/%Y')
            
            html = '<table class="table table-striped table-sm">'
            html += '<thead><tr><th>Fecha (Semana)</th><th>Producto</th><th>Cantidad Total</th></tr></thead>'
            html += '<tbody>'
            
            for _, row in df_display.iterrows():
                html += f'<tr><td>{row["fecha"]}</td><td>{row["producto"]}</td><td>{int(row["cantidad"])}</td></tr>'
            
            html += '</tbody></table>'
            html += f'<small class="text-muted">Mostrando primeras 10 filas procesadas</small>'
            
            return html
            
        except Exception as e:
            return f'<p class="text-danger">Error al generar preview: {str(e)}</p>'