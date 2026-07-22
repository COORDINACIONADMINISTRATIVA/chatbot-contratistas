import os
import pandas as pd
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_CORREOS = os.path.join(BASE_DIR, 'database', 'correos_contratistas.xlsx')

class LectorCorreos:
    def __init__(self):
        self.df = None
        self.cargar_datos()

    def cargar_datos(self):
        try:
            if not os.path.exists(RUTA_CORREOS):
                print(f"⚠️ No se encontró el archivo de correos: {RUTA_CORREOS}")
                return
            
            self.df = pd.read_excel(RUTA_CORREOS)
            print(f"📊 Correos cargados: {len(self.df)} registros")
            
            # Limpiar nombres de columnas
            self.df.columns = [str(col).strip().upper() for col in self.df.columns]
            
            # Buscar columnas necesarias
            col_correo = None
            col_cedula = None
            col_nombre = None
            for col in self.df.columns:
                if 'CORREO' in col or 'EMAIL' in col or 'MAIL' in col:
                    col_correo = col
                if 'CÉDULA' in col or 'CEDULA' in col or 'DOCUMENTO' in col:
                    col_cedula = col
                if 'NOMBRE' in col:
                    col_nombre = col
            
            if col_correo is None or col_cedula is None:
                print("❌ Columnas necesarias no encontradas: correo y cédula")
                return
            
            # Limpiar datos
            self.df['CEDULA'] = self.df[col_cedula].astype(str).apply(lambda x: re.sub(r'[^\d]', '', x))
            self.df['CORREO'] = self.df[col_correo].astype(str).apply(lambda x: x.strip() if '@' in x else None)
            self.df['NOMBRE'] = self.df[col_nombre] if col_nombre else None
            
            # Filtrar filas con correo válido
            self.df = self.df[self.df['CORREO'].notna()]
            self.df = self.df[self.df['CEDULA'].str.len() >= 6]
            
            print(f"✅ {len(self.df)} correos válidos encontrados")
            
        except Exception as e:
            print(f"❌ Error cargando correos: {e}")

    def obtener_correos(self):
        """Devuelve lista de dicts con cedula, correo, nombre"""
        if self.df is None or self.df.empty:
            return []
        
        correos = []
        for _, row in self.df.iterrows():
            item = {
                'cedula': row['CEDULA'],
                'correo': row['CORREO'],
                'nombre': row.get('NOMBRE', None)
            }
            correos.append(item)
        return correos

# Instancia global
lector_correos = LectorCorreos()