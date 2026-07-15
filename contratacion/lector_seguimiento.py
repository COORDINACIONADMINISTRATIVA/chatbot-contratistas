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
                print(f"⚠️ No se encontró el archivo de seguimiento")
                return
            
            self.df = pd.read_excel(RUTA_SEGUIMIENTO)
            print(f"📊 Seguimiento cargado: {len(self.df)} registros")
            
            # Limpiar nombres de columnas
            self.df.columns = [str(col).replace('\xa0', ' ').strip().upper() for col in self.df.columns]
            
            # Buscar la columna que contiene el texto de posición (puede llamarse "TEXTO DE POS" o "TEXTO POS")
            col_texto_pos = None
            for col in self.df.columns:
                if 'TEXTO' in col and 'POS' in col:
                    col_texto_pos = col
                    break
            
            if col_texto_pos is None:
                print("⚠️ No se encontró columna de 'Texto de Pos' en el Excel de seguimiento")
                return
            
            # Crear la columna CEDULA extrayendo del texto de posición
            self.df['CEDULA'] = self.df[col_texto_pos].apply(
                lambda x: self._extraer_cedula_desde_texto(str(x)) if pd.notna(x) else ''
            )
            
            print(f"✅ Columna CEDULA creada a partir de '{col_texto_pos}'")
            print(f"   Ejemplo: {self.df['CEDULA'].iloc[0] if len(self.df) > 0 else 'sin datos'}")
            
        except Exception as e:
            print(f"❌ Error cargando seguimiento: {e}")

    def _extraer_cedula_desde_texto(self, texto):
        """Extrae la cédula del texto de posición (busca CÉDULA o IDENTIFICACION)"""
        if not texto:
            return ''
        # Buscar tanto "CÉDULA" como "IDENTIFICACION"
        match = re.search(r'(?:C[ÉE]DULA|IDENTIFICACION)\s*[:]?\s*(\d{6,12})', texto, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ''

    def buscar_por_cedula(self, cedula):
        if self.df is None:
            return []
        
        cedula_limpia = re.sub(r'[^\d]', '', str(cedula))
        if not cedula_limpia or len(cedula_limpia) < 6:
            return []
        
        resultados = self.df[self.df['CEDULA'] == cedula_limpia]
        return resultados.to_dict('records') if len(resultados) > 0 else []

    def extraer_info_pos(self, texto):
        """Extrae nombre, cédula, tipo de pago, mes y objeto del texto de posición"""
        if not texto or pd.isna(texto):
            return {}
        
        texto = str(texto)
        datos = {}
        
        # Detectar tipo de contrato
        if 'RENOVACIÓN LICENCIA' in texto.upper() or 'LICENCIA' in texto.upper():
            datos['tipo'] = 'licencia'
            match = re.search(r'LICENCIA\s+\d+\s+MES\s+(\w+)', texto, re.IGNORECASE)
            if match:
                datos['mes_licencia'] = match.group(1).upper()
            objeto = re.sub(r'\s*LICENCIA\s+\d+\s+MES\s+\w+.*$', '', texto, flags=re.IGNORECASE)
            datos['objeto'] = objeto.strip()
        else:
            datos['tipo'] = 'servicio'
            # Extraer nombre
            match = re.search(r'NOMBRE\s*[:]?\s*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s\.]+?)(?=\s*(?:C[ÉE]DULA|IDENTIFICACION)|\s*$)', texto, re.IGNORECASE)
            if match:
                datos['nombre'] = match.group(1).strip()
            # Extraer cédula (acepta CÉDULA o IDENTIFICACION)
            match = re.search(r'(?:C[ÉE]DULA|IDENTIFICACION)\s*[:]?\s*(\d{6,12})', texto, re.IGNORECASE)
            if match:
                datos['cedula'] = match.group(1).strip()
            # Extraer tipo de pago (corrigiendo errores)
            match = re.search(r'(PRIMER|SEGUNDO|TERCER|CUARTO|QUINTO|ÚNICO|UNICO)\s*PAGO', texto, re.IGNORECASE)
            if match:
                tipo = match.group(1).upper()
                if 'TERCER SEGUNDO' in texto.upper():
                    tipo = 'TERCER PAGO'
                datos['tipo_pago'] = tipo
            # Extraer objeto (descripción completa, sin nombre/cedula/pago)
            objeto = re.sub(r'NOMBRE\s*[:]?\s*[A-ZÁÉÍÓÚÑ\s\.]+', '', texto, flags=re.IGNORECASE)
            objeto = re.sub(r'(?:C[ÉE]DULA|IDENTIFICACION)\s*[:]?\s*\d{6,12}', '', objeto)
            objeto = re.sub(r'(PRIMER|SEGUNDO|TERCER|CUARTO|QUINTO|ÚNICO|UNICO)\s*PAGO', '', objeto, flags=re.IGNORECASE)
            datos['objeto'] = objeto.strip()
        
        return datos

# Instancia global
lector_seguimiento = LectorSeguimiento()