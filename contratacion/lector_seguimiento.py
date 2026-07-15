import os
import re
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_SEGUIMIENTO = os.path.join(BASE_DIR, 'database', 'seguimiento.xlsx')

class LectorSeguimiento:
    def __init__(self):
        self.df = None
        self.cargar_datos()

    def cargar_datos(self):
        try:
            if not os.path.exists(RUTA_SEGUIMIENTO):
                print("⚠️ No se encontró el archivo de seguimiento")
                return
            
            self.df = pd.read_excel(RUTA_SEGUIMIENTO)
            print(f"📊 Seguimiento cargado: {len(self.df)} registros")
            
            # Limpiar nombres de columnas: eliminar \xa0, espacios extra, y pasar a mayúsculas
            self.df.columns = [
                str(col).replace('\xa0', ' ').replace('\n', ' ').strip().upper()
                for col in self.df.columns
            ]
            
            print(f"📋 Columnas disponibles: {list(self.df.columns)}")
            
            # Buscar la columna que contiene la cédula
            col_documento = None
            for col in self.df.columns:
                if 'DOCUMENTO' in col or 'IDENTIDAD' in col or 'CÉDULA' in col or 'CEDULA' in col:
                    col_documento = col
                    break
            
            if col_documento:
                print(f"✅ Columna de documento detectada: '{col_documento}'")
                # Crear columna CEDULA limpia
                self.df['CEDULA'] = (
                    self.df[col_documento]
                    .astype(str)
                    .apply(lambda x: re.sub(r'[^\d]', '', str(x)))
                )
                # Filtrar filas con cédula vacía o muy corta
                self.df = self.df[self.df['CEDULA'].str.len() >= 6]
                print(f"✅ {len(self.df)} registros con cédula válida")
            else:
                print("⚠️ No se encontró una columna de documento de identidad")
                
        except Exception as e:
            print(f"❌ Error cargando seguimiento: {e}")
            import traceback
            traceback.print_exc()
    
    def buscar_por_cedula(self, cedula):
        if self.df is None:
            return []
        
        cedula_limpia = re.sub(r'[^\d]', '', str(cedula))
        if not cedula_limpia or len(cedula_limpia) < 6:
            return []
        
        resultados = self.df[self.df['CEDULA'] == cedula_limpia]
        return resultados.to_dict('records') if len(resultados) > 0 else []

def extraer_info_pos(texto):
    if not texto or pd.isna(texto):
        return {}
    
    texto = str(texto)
    datos = {}
    
    # Detectar tipo de contrato
    if 'RENOVACI' in texto.upper() or 'LICENCIA' in texto.upper():
        datos['tipo'] = 'licencia'
        # Extraer mes de licencia: "LICENCIA 1 MES ENERO" -> "ENERO"
        match = re.search(r'LICENCIA\s+\d+\s+MES\s+(\w+)', texto, re.IGNORECASE)
        if match:
            datos['mes_licencia'] = match.group(1).upper()
        # Extraer el objeto (descripción completa)
        objeto = re.sub(r'\s*LICENCIA\s+\d+\s+MES\s+\w+.*$', '', texto, flags=re.IGNORECASE)
        datos['objeto'] = objeto.strip()
    else:
        datos['tipo'] = 'servicio'
        # Extraer nombre
        match = re.search(r'NOMBRE\s*[:]?\s*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s\.]+?)(?=\s*C[ÉE]DULA|\s*$)', texto, re.IGNORECASE)
        if match:
            datos['nombre'] = match.group(1).strip()
        # Extraer cédula
        match = re.search(r'C[ÉE]DULA\s*[:]?\s*(\d{6,12})', texto, re.IGNORECASE)
        if match:
            datos['cedula'] = match.group(1).strip()
        # Extraer tipo de pago (corrigiendo errores)
        match = re.search(r'(PRIMER|SEGUNDO|TERCER|CUARTO|QUINTO|ÚNICO|UNICO)\s*PAGO', texto, re.IGNORECASE)
        if match:
            tipo = match.group(1).upper()
            # Corregir error tipográfico: "TERCER SEGUNDO" no existe, probablemente "TERCER PAGO"
            if 'TERCER SEGUNDO' in texto.upper():
                tipo = 'TERCER PAGO'
            datos['tipo_pago'] = tipo
        # Extraer objeto (descripción completa, sin nombre/cedula/pago)
        objeto = re.sub(r'NOMBRE\s*[:]?\s*[A-ZÁÉÍÓÚÑ\s\.]+', '', texto, flags=re.IGNORECASE)
        objeto = re.sub(r'C[ÉE]DULA\s*[:]?\s*\d{6,12}', '', objeto)
        objeto = re.sub(r'(PRIMER|SEGUNDO|TERCER|CUARTO|QUINTO|ÚNICO|UNICO)\s*PAGO', '', objeto, flags=re.IGNORECASE)
        datos['objeto'] = objeto.strip()
    
    return datos

def limpiar_texto_pos(texto):
    # Eliminar saltos de línea excesivos, espacios, etc.
    texto = re.sub(r'\n+', '\n', texto)
    texto = re.sub(r' +', ' ', texto)
    return texto.strip()

# Instancia global
lector_seguimiento = LectorSeguimiento()