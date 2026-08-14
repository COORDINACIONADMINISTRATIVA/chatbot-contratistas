"""
Simula usuarios reales abriendo la página /consultas, escribiendo una pregunta
y esperando la respuesta del chatbot.

Mide el tiempo total desde que abre la página hasta que recibe la respuesta.

Uso:
    python3 prueba_carga_consultas_completas.py --url https://chatbot-contratistas-1.onrender.com --usuarios 200
"""

import argparse
import time
import concurrent.futures
import statistics
import urllib.request
import json
import threading

# Preguntas que los usuarios van a enviar
PREGUNTAS = [
    "80020175",
    "79637489",
    "52501269",
    "1010198590",
    "52544139",
    "1",
    "2",
    "1",
    "1",
    "1"
]

def abrir_pagina_y_preguntar(url_base, usuario_id):
    """
    Simula un usuario real:
    1. Abre la página /consultas.
    2. Escribe una pregunta.
    3. Hace clic en enviar.
    4. Espera la respuesta.
    5. Mide el tiempo total.
    """
    inicio_total = time.time()
    
    try:
        # PASO 1: Abrir la página /consultas (GET)
        url_consultas = url_base.rstrip("/") + "/consultas"
        req_get = urllib.request.Request(url_consultas, method="GET")
        with urllib.request.urlopen(req_get, timeout=30) as resp_get:
            status_get = resp_get.status
            # Leemos el HTML (para simular que el navegador lo procesa)
            html = resp_get.read()
        
        # PASO 2: Simular que el usuario escribe una pregunta
        pregunta = PREGUNTAS[usuario_id % len(PREGUNTAS)]
        usuario = f"prueba_{usuario_id}"
        
        # PASO 3: Enviar la pregunta al chatbot (POST /api/chat)
        url_chat = url_base.rstrip("/") + "/api/chat"
        body = json.dumps({
            "mensaje": pregunta,
            "usuario": usuario
        }).encode("utf-8")
        req_post = urllib.request.Request(
            url_chat,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req_post, timeout=60) as resp_post:
            status_post = resp_post.status
            respuesta = resp_post.read()
        
        # PASO 4: Simular que el usuario lee la respuesta (pequeña pausa)
        time.sleep(0.1)
        
        status = f"GET:{status_get} POST:{status_post}"
        exito = (status_get == 200 and status_post == 200)
        
    except Exception as e:
        status = f"ERROR: {e}"
        exito = False
    
    duracion_total = time.time() - inicio_total
    return usuario_id, status, duracion_total, exito

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url_posicional", nargs="?", default=None, help="URL base de la app")
    parser.add_argument("--url", default=None, help="URL base de la app")
    parser.add_argument("--usuarios", type=int, default=20, help="Número de usuarios simultáneos")
    args = parser.parse_args()

    url_base = args.url or args.url_posicional or "http://localhost:5000"
    print(f"Simulando {args.usuarios} usuarios abriendo {url_base}/consultas y enviando preguntas...\n")

    inicio_total = time.time()
    resultados = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.usuarios) as executor:
        futuros = [
            executor.submit(abrir_pagina_y_preguntar, url_base, i)
            for i in range(args.usuarios)
        ]
        for f in concurrent.futures.as_completed(futuros):
            resultados.append(f.result())
    
    total = time.time() - inicio_total
    
    resultados.sort(key=lambda r: r[0])
    exitosos = [r for r in resultados if r[3]]
    fallidos = [r for r in resultados if not r[3]]
    
    print(f"{'usuario':<10}{'status':<30}{'tiempo (s)':<10}")
    for usuario_id, status, duracion, _ in resultados:
        print(f"{usuario_id:<10}{status:<30}{duracion:.2f}")
    
    print("\n" + "=" * 50)
    print(f"Total: {len(resultados)} usuarios completados en {total:.2f}s")
    print(f"Exitosos (GET 200 + POST 200): {len(exitosos)}")
    print(f"Fallidos/timeout: {len(fallidos)}")
    if exitosos:
        tiempos = [r[2] for r in exitosos]
        print(f"Tiempo promedio por usuario: {statistics.mean(tiempos):.2f}s")
        print(f"Tiempo mínimo:   {min(tiempos):.2f}s")
        print(f"Tiempo máximo:   {max(tiempos):.2f}s")
    print("=" * 50)

if __name__ == "__main__":
    main()