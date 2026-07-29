# chatbot/motor.py - VERSIÓN SIMPLE Y FUNCIONAL
# SIN FLUJOS, SIN ORQUESTADOR, SOLO RESPUESTAS DIRECTAS

import re
import random
from .memoria import memoria
from .conocimiento.rut import PATRONES_RUT, respuesta_rut
from .conocimiento.documentos import PATRONES_DOCUMENTOS, respuesta_documentos
from .conocimiento.portal import PATRONES_PORTAL, respuesta_portal
from .conocimiento.contratos import PATRONES_CONTRATOS, respuesta_contratos
from .respuestas_campos import RESPUESTAS_CAMPOS
from .respuestas import RESPUESTAS
from .detector import extraer_cedula
from .navegador import formatear_menu_principal

# ============================================================
# RESPUESTAS COMPLETAS POR TEMA
# ============================================================

RESPUESTAS_COMPLETAS = {
    "documentos": """📋 **DOCUMENTOS REQUERIDOS PARA CONTRATAR**

Los documentos dependen de su tipo de contratación:

📌 **PERSONA NATURAL (INDEPENDIENTE):**
1. 📄 Cédula de ciudadanía (ambas caras, PDF)
2. 🏦 Certificación bancaria (máx. 30 días, PDF)
3. 📋 RUT actualizado (máx. 30 días, PDF)
4. 📊 Formato Excel "Ingreso Independientes"
5. 🏥 Certificación ARL activa (PDF)
6. 🏥 Examen médico ocupacional (máx. 3 años, PDF)

📌 **EMPRESA / PERSONA JURÍDICA:**
1. 📄 Cédula del representante legal (ambas caras)
2. 🏦 Certificación bancaria de la empresa (máx. 30 días)
3. 📋 RUT de la empresa actualizado (máx. 30 días)
4. 📑 Cámara de Comercio (máx. 30 días)
5. 🏥 Certificación ARL de la empresa
6. 🏥 Examen médico del representante (máx. 3 años)

⚠️ **TODOS en PDF y sin contraseña.**

¿Es persona natural o empresa?""",

    "rut": """📝 **INFORMACIÓN SOBRE EL RUT**

El RUT (Registro Único Tributario) es su identificación ante la DIAN.

🔹 **REQUISITOS PARA CONTRATAR:**
- ✅ Fecha de expedición: **menor a 30 días**
- ✅ Marca de agua: **"Copia" o "Certificado"**
- ✅ Actividad económica: **8560** (recomendada)

🔹 **¿CÓMO ACTUALIZARLO?**
1. Ingrese a www.dian.gov.co
2. Inicie sesión con su usuario
3. Busque "Actualización RUT"
4. Revise y actualice sus datos
5. Descargue con marca "Copia" o "Certificado"

🔹 **¿QUÉ PASA SI ESTÁ "EN TRÁMITE"?**
- NO es válido. Debe esperar a que la DIAN lo apruebe (24-72 horas).

¿Necesita ayuda con algún paso específico?""",

    "arl": """🏥 **INFORMACIÓN SOBRE ARL**

La ARL protege a los trabajadores contra accidentes laborales.

🔹 **ES OBLIGATORIA** para todos los contratistas.

🔹 **ARL RECOMENDADAS:**
- Positiva
- Sura
- Colmena
- AXA Colpatria
- Seguros Bolívar
- La Equidad

🔹 **¿CÓMO OBTENER LA CERTIFICACIÓN?**
1. Comuníquese con su ARL
2. Solicite certificación de afiliación
3. Indique que es para contratar con UNIMINUTO
4. Solicítela en PDF sin contraseña

🔹 **¿QUÉ PASA SI NO TENGO ARL?**
- No puede contratar. Debe afiliarse antes de iniciar.

¿Necesita ayuda para afiliarse?""",

    "examen_medico": """🏥 **EXAMEN MÉDICO OCUPACIONAL**

🔹 **ES OBLIGATORIO** para todos los contratistas.
🔹 **VIGENCIA MÁXIMA:** 3 años

🔹 **¿DÓNDE HACERLO?**
- ARL (Administradora de Riesgos Laborales)
- Clínicas ocupacionales
- IPS autorizadas

🔹 **COSTO:** $50,000 - $150,000

🔹 **REQUISITOS:**
- El certificado debe decir **APTO** para el cargo
- Formato PDF sin contraseña

Si su examen tiene más de 3 años, debe renovarlo.""",

    "portal": """🌐 **REGISTRO EN EL PORTAL DE PROVEEDORES**

🔹 **ACCESO:** https://proveedores.uniminuto.edu

🔹 **CAMPOS CLAVE:**
- **Sede:** "Rectoría UNIMINUTO Virtual" (PRIMERA OPCIÓN)
- **Bien o Servicio:** "Servicio"
- **Tratamiento:** "Señor(a)" o "Empleado(a)"
- **Régimen:** "Simplificado" (natural) o "Común" (empresa)
- **Correo:** El mismo de su RUT
- **Código Postal:** Busque el de su ciudad en Google

🔹 **PROBLEMAS COMUNES:**
- ❌ No carga la página → pruebe con otro navegador
- ❌ Error al registrarse → revise la sede, régimen y tratamiento
- ❌ No recibe correo → revise la carpeta de spam

💡 **RECUERDE:** Después de registrarse, debe enviar los documentos requeridos.

¿Necesita ayuda con algún campo en específico?""",

    "contrato": """📝 **INFORMACIÓN SOBRE CONTRATOS**

🔹 **ASPECTOS CLAVE DEL CONTRATO:**
- **Objeto:** qué va a hacer
- **Duración:** fechas de inicio y fin
- **Entregables:** qué productos debe entregar
- **Valor:** cuánto le pagan
- **Forma de pago:** cómo y cuándo pagan
- **Supervisor:** quién lo supervisa

🔹 **¿CÓMO FIRMAR?**
1. Recibirá un correo con el contrato
2. Lea TODO el contrato con atención
3. Firme digitalmente (en el portal o con certificado)
4. Recibirá confirmación y copia firmada

🔹 **PROBLEMAS COMUNES:**
- "No me llega el correo" → revise spam, verifique su correo
- "No puedo abrir el enlace" → use Chrome/Firefox, limpie caché
- "La firma no se completa" → verifique su conexión a internet

¿Necesita ayuda con algún aspecto específico?"""
}

# ============================================================
# PALABRAS CLAVE POR TEMA
# ============================================================

PALABRAS_TEMA = {
    "rut": ['rut', 'actualizar rut', 'renovar rut', 'rut vencido', 'rut nuevo'],
    "arl": ['arl', 'afiliarme', 'riesgos laborales', 'arl activa'],
    "examen_medico": ['examen medico', 'examen ocupacional', 'examen de ingreso', 'examen laboral'],
    "portal": ['portal', 'proveedores', 'registro', 'plataforma', 'inscribirme'],
    "documentos": ['documentos', 'papeles', 'requisitos', 'que necesito', 'que me piden', 'qué papeles', 'documentación'],
    "contrato": ['contrato', 'firma', 'firmar', 'supervisor', 'pagos', 'firma digital'],
}

PALABRAS_SALUDO = ['hola', 'buenos', 'buenas', 'saludos', 'buen día', 'buenas tardes', 'hey', 'que tal']

# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def responder(mensaje, usuario="anonimo"):
    """
    Punto de entrada principal - Responde TODO directamente
    """
    mensaje_lower = mensaje.lower()
    
    # Guardar en memoria
    memoria.guardar_mensaje(usuario, mensaje, tipo="usuario")
    
    # ============================================================
    # 1. RUT
    # ============================================================
    if any(p in mensaje_lower for p in PATRONES_RUT) or 'rut' in mensaje_lower:
        respuesta = respuesta_rut(mensaje)
        if respuesta and len(respuesta) > 30:
            return respuesta
        return RESPUESTAS_COMPLETAS["rut"]
    
    # ============================================================
    # 2. ARL
    # ============================================================
    if any(p in mensaje_lower for p in PALABRAS_TEMA["arl"]):
        if 'arl' in RESPUESTAS and RESPUESTAS.get('arl'):
            return random.choice(RESPUESTAS['arl'])
        return RESPUESTAS_COMPLETAS["arl"]
    
    # ============================================================
    # 3. EXAMEN MÉDICO
    # ============================================================
    if any(p in mensaje_lower for p in PALABRAS_TEMA["examen_medico"]):
        if 'examen_medico' in RESPUESTAS and RESPUESTAS.get('examen_medico'):
            return random.choice(RESPUESTAS['examen_medico'])
        return RESPUESTAS_COMPLETAS["examen_medico"]
    
    # ============================================================
    # 4. DOCUMENTOS
    # ============================================================
    if any(p in mensaje_lower for p in PALABRAS_TEMA["documentos"]):
        respuesta = respuesta_documentos(mensaje)
        if respuesta and len(respuesta) > 30:
            return respuesta
        return RESPUESTAS_COMPLETAS["documentos"]
    
    # ============================================================
    # 5. PORTAL
    # ============================================================
    if any(p in mensaje_lower for p in PALABRAS_TEMA["portal"]):
        respuesta = respuesta_portal(mensaje)
        if respuesta and len(respuesta) > 30:
            return respuesta
        return RESPUESTAS_COMPLETAS["portal"]
    
    # ============================================================
    # 6. CONTRATOS / FIRMA
    # ============================================================
    if any(p in mensaje_lower for p in PALABRAS_TEMA["contrato"]):
        respuesta = respuesta_contratos(mensaje)
        if respuesta and len(respuesta) > 30:
            return respuesta
        return RESPUESTAS_COMPLETAS["contrato"]
    
    # ============================================================
    # 7. CAMPOS DEL FORMULARIO
    # ============================================================
    for campo, respuesta in RESPUESTAS_CAMPOS.items():
        if campo in mensaje_lower or campo.replace('_', ' ') in mensaje_lower:
            return respuesta
    
    # ============================================================
    # 8. CÉDULA (CONSULTAR ESTADO)
    # ============================================================
    cedula = extraer_cedula(mensaje)
    if cedula:
        try:
            from contratacion.lector import lector
            registros = lector.buscar_por_cedula(cedula)
            if registros:
                info = lector.obtener_info_contratista(registros[0])
                return f"""📋 **ESTADO DE SU PROCESO**

👤 **Nombre:** {info.get('nombre', 'Sin nombre')}
🆔 **Cédula:** {info.get('cedula', cedula)}
📊 **Estado:** {info.get('estado', 'Sin estado')}

📝 **Observación:**
{info.get('observacion', 'Sin observaciones')}

¿En qué más le puedo ayudar?"""
            else:
                return f"❌ No encontré información con la cédula {cedula}.\n\nVerifique que el número esté bien escrito."
        except Exception as e:
            return f"❌ Error al buscar: {str(e)}"
    
    # ============================================================
    # 9. SALUDO
    # ============================================================
    if any(p in mensaje_lower for p in PALABRAS_SALUDO):
        return """👋 ¡Hola! Soy el asistente de contratación de UNIMINUTO Virtual.

**Puedo ayudarle con estos temas:**

📋 **Documentos** (qué necesita según su tipo)
🌐 **Portal de proveedores** (cómo registrarse)
📝 **RUT** (cómo actualizarlo, requisitos)
🏥 **ARL** (cómo afiliarse, certificación)
🏥 **Examen médico** (dónde hacerlo, vigencia)
📝 **Contratos** (firma, supervisor, pagos)

🔍 **Para consultar su estado**, escriba su número de cédula.

**¿En qué tema específico necesita ayuda?**"""
    
    # ============================================================
    # 10. RESPUESTA POR DEFECTO
    # ============================================================
    return """No entendí bien su pregunta. 😅

**Puedo ayudarle con estos temas:**
📋 Documentos
🌐 Portal de proveedores
📝 RUT
🏥 ARL
🏥 Examen médico
📝 Contratos

**Escriba el tema que le interesa** o su número de cédula para consultar su estado."""