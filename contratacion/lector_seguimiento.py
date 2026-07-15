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
            
            # Limpiar columnas
            self.df.columns = [str(col).replace('\xa0', ' ').strip().upper() for col in self.df.columns]
            
            # Limpiar cédulas
            if 'DOCUMENTO DE IDENTIDAD' in self.df.columns:
                self.df['CEDULA'] = self.df['DOCUMENTO DE IDENTIDAD'].astype(str).apply(
                    lambda x: re.sub(r'[^\d]', '', str(x))
                )
                
        except Exception as e:
            print(f"❌ Error cargando seguimiento: {e}")
    
    def buscar_por_cedula(self, cedula):
        if self.df is None:
            return []
        
        cedula_limpia = re.sub(r'[^\d]', '', str(cedula))
        resultados = self.df[self.df['CEDULA'] == cedula_limpia]
        return resultados.to_dict('records') if len(resultados) > 0 else []
    
    def extraer_info_pos(self, texto):
        """Extrae nombre, cédula y tipo de pago del texto de POS"""
        if not texto or pd.isna(texto):
            return {}
        
        texto = str(texto)
        datos = {}
        
        # Extraer nombre
        match = re.search(r'NOMBRE\s*[:]?\s*([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s\.]+?)(?:\s*[-–]|\s*C[ÉE]DULA|\s*$)', texto, re.IGNORECASE)
        if match:
            datos['nombre'] = match.group(1).strip()
        
        # Extraer cédula
        match = re.search(r'C[ÉE]DULA\s*[:]?\s*(\d{6,12})', texto, re.IGNORECASE)
        if match:
            datos['cedula'] = match.group(1).strip()
        
        # Extraer tipo de pago
        match = re.search(r'(PRIMER|SEGUNDO|TERCER|CUARTO|QUINTO|SEXTO|SÉPTIMO|OCTAVO|NOVENO|DÉCIMO|ÚNICO|UNICO)\s*PAGO', texto, re.IGNORECASE)
        if match:
            datos['tipo_pago'] = match.group(1).upper() + " PAGO"
        
        # Extraer mes (si aparece)
        meses = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
        for mes in meses:
            if mes in texto.upper():
                datos['mes'] = mes.capitalize()
                break
        
        return datos

lector_seguimiento = LectorSeguimiento()