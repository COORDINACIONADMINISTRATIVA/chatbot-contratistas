"""
Prueba rápida y manual del lector/validador de RUT.
Uso: python test_lector_pdf.py [ruta_al_rut.pdf] [cedula_esperada]
"""
import sys
from contratacion.validador_rut import validar_rut_archivo

ruta = sys.argv[1] if len(sys.argv) > 1 else "RUT.pdf"
cedula = sys.argv[2] if len(sys.argv) > 2 else ""

respuesta, resultados = validar_rut_archivo(ruta, cedula)
print(respuesta)
print("\nVALIDO:", resultados["valido"])
