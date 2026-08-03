"""
Lector de Excel de contratistas - Versión mejorada
"""
import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_EXCEL = os.path.join(BASE_DIR, 'database', 'contratacion.xlsx')


class LectorContratistas:
    def __init__(self):
        self.df = None
        self.columnas = {}
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga el Excel y limpia las columnas"""
        try:
            if not os.path.exists(RUTA_EXCEL):
                print(f"⚠️ No se encontró el archivo: {RUTA_EXCEL}")
                return False
            
            self.df = pd.read_excel(RUTA_EXCEL)
            print(f"📊 Excel cargado: {len(self.df)} filas")
            
            # Limpiar nombres de columnas (quitar espacios raros como \xa0)
            self.df.columns = [
                str(col).replace('\xa0', ' ').replace('\n', ' ').strip().upper()
                for col in self.df.columns
            ]
            
            # Mapear las columnas que necesitamos
            for col in self.df.columns:
                col_upper = col.upper()
                if 'AÑO' in col_upper or 'ANO' in col_upper:
                    self.columnas['año'] = col
                elif 'NOMBRE' in col_upper and 'CONTRATISTA' in col_upper:
                    self.columnas['nombre'] = col
                elif 'DOCUMENTO' in col_upper or 'IDENTIDAD' in col_upper or 'CÉDULA' in col_upper or 'CEDULA' in col_upper:
                    self.columnas['documento'] = col
                elif 'ESTADO' in col_upper:
                    self.columnas['estado'] = col
                elif 'OBSERV' in col_upper:
                    self.columnas['observacion'] = col
                elif 'FECHA_INICIO' in col_upper:
                    self.columnas['fecha_inicio'] = col
                elif 'FECHA_FIN' in col_upper:
                    self.columnas['fecha_fin'] = col
                elif 'OBJETO' in col_upper and 'CONTRATO' in col_upper:
                    self.columnas['objeto'] = col
                elif 'CONTRATO' in col_upper and 'OBJETO' not in col_upper:  # <--- CAMBIO AQUÍ
                    self.columnas['solicitud_ariba'] = col

            print(f"📋 Columnas mapeadas: {self.columnas}")
            
            # Crear columna CEDULA limpia
            if 'documento' in self.columnas:
                self.df['CEDULA'] = (
                    self.df[self.columnas['documento']]
                    .astype(str)
                    .apply(lambda x: re.sub(r'[^\d]', '', str(x)))
                )
                # Eliminar filas donde CEDULA quedó vacía o muy corta
                self.df = self.df[self.df['CEDULA'].str.len() >= 6]
                print(f"✅ {len(self.df)} contratistas con cédula válida")
            
            return True
            
        except Exception as e:
            print(f"❌ Error cargando Excel: {e}")
            return False
    
    def buscar_por_cedula(self, cedula):
        """Busca un contratista por su cédula"""
        if self.df is None:
            print("⚠️ DataFrame no cargado")
            return None
        
        try:
            # Limpiar la cédula buscada (solo números)
            cedula_limpia = re.sub(r'[^\d]', '', str(cedula))
            
            if not cedula_limpia or len(cedula_limpia) < 6:
                return None
            
            # Buscar coincidencia exacta
            resultados = self.df[self.df['CEDULA'] == cedula_limpia]
            
            if len(resultados) == 0:
                # Intentar búsqueda flexible (últimos N dígitos)
                if len(cedula_limpia) >= 7:
                    cedula_corta = cedula_limpia[-7:]  # últimos 7 dígitos
                    resultados = self.df[self.df['CEDULA'].str.endswith(cedula_corta)]
            
            if len(resultados) == 0:
                return None
            
            return resultados.to_dict('records')
            
        except Exception as e:
            print(f"Error en buscar_por_cedula: {e}")
            return None
    
    def buscar_por_nombre(self, nombre):
        """Busca contratistas por nombre"""
        if self.df is None:
            return []
        
        try:
            nombre_lower = str(nombre).lower().strip()
            if not nombre_lower:
                return []
            
            col = self.columnas.get('nombre', 'NOMBRE DE CONTRATISTA')
            if col not in self.df.columns:
                return []
            
            resultados = self.df[
                self.df[col]
                .astype(str)
                .str.lower()
                .str.contains(nombre_lower, na=False)
            ]
            
            return resultados.to_dict('records')
            
        except Exception as e:
            print(f"Error en buscar_por_nombre: {e}")
            return []
    
    def obtener_info_contratista(self, registro):
        """Extrae la información formateada de un registro"""
        info = {
            'nombre': 'Sin nombre',
            'cedula': '',
            'estado': 'Sin estado',
            'observacion': 'Sin observaciones',
            'año': '',
            'fecha_inicio': '',
            'fecha_fin': '',
            'objeto': '',
            'solicitud_ariba': '-'
        }
        
        try:
            if 'nombre' in self.columnas:
                col = self.columnas['nombre']
                if col in registro:
                    info['nombre'] = str(registro.get(col, 'Sin nombre'))
            
            if 'documento' in self.columnas:
                col = self.columnas['documento']
                if col in registro:
                    doc = str(registro.get(col, ''))
                    info['cedula'] = re.sub(r'[^\d]', '', doc)
            
            if 'estado' in self.columnas:
                col = self.columnas['estado']
                if col in registro:
                    info['estado'] = str(registro.get(col, 'Sin estado'))
            
            if 'observacion' in self.columnas:
                col = self.columnas['observacion']
                if col in registro:
                    info['observacion'] = str(registro.get(col, 'Sin observaciones'))
            
            if 'año' in self.columnas:
                col = self.columnas['año']
                if col in registro:
                    info['año'] = str(registro.get(col, ''))
            
            if 'fecha_inicio' in self.columnas:
                col = self.columnas['fecha_inicio']
                if col in registro and pd.notna(registro.get(col)):
                    info['fecha_inicio'] = str(registro.get(col, ''))
            
            if 'fecha_fin' in self.columnas:
                col = self.columnas['fecha_fin']
                if col in registro and pd.notna(registro.get(col)):
                    info['fecha_fin'] = str(registro.get(col, ''))
            
            if 'objeto' in self.columnas:
                col = self.columnas['objeto']
                if col in registro and pd.notna(registro.get(col)):
                    info['objeto'] = str(registro.get(col, ''))

            # ===== EXTRACCIÓN DE CONTRATO (CORREGIDO) =====
            if 'solicitud_ariba' in self.columnas:
                col = self.columnas['solicitud_ariba']
                if col in registro and pd.notna(registro.get(col)):
                    valor = str(registro.get(col, '')).strip()
                    # Limpiar caracteres especiales
                    valor = valor.replace('"', '').replace("'", '').strip()
                    
                    # 1. Buscar CPS o DIEPO CPS (ej: CPS 438-2025, DIEPO CPS 768-2026)
                    match_cps = re.search(r'(DIEPO\s*CPS|CPS|CONTRATO\s*DE\s*ARRENDAMIENTO|OTROSI)[\s\-]*\d{0,4}[\s\-]*\d{4}', valor.upper())
                    if match_cps:
                        info['solicitud_ariba'] = match_cps.group(0)
                    else:
                        # 2. Buscar OTROSI (ej: OTROSI No.1 - CPS 680-2025)
                        match_otrosi = re.search(r'(OTROSI[^\d]*\d+[^\d]*(?:CPS[\s-]?\d{3,}[\s-]?\d{4}))', valor.upper())
                        if match_otrosi:
                            info['solicitud_ariba'] = match_otrosi.group(0)
                        else:
                            # 3. Si no tiene CPS ni OTROSI, verificar si es "NO APLICA"
                            if valor and 'NO APLICA' not in valor.upper():
                                # Si tiene algún texto que parezca número de contrato, guardarlo
                                info['solicitud_ariba'] = valor
                            # Si es "NO APLICA" o está vacío, queda como '-'
                            
        except Exception as e:
            print(f"Error en obtener_info: {e}")
        
        return info


# Instancia global
lector = LectorContratistas()