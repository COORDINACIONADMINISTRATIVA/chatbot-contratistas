"""
Simula varios usuarios mandando preguntas al chat (/api/chat) al mismo tiempo,
para ver el comportamiento real bajo carga concurrente (no secuencial).

Uso:
    python3 prueba_carga_chat.py --url https://tu-app.onrender.com --usuarios 20

Si no le pasas --url, prueba contra http://localhost:5000 (útil para probar
local antes de pegarle al de Render).
"""

import argparse
import time
import concurrent.futures
import statistics
import urllib.request
import json

PREGUNTAS = [
    "1",
    "2",
    "3",
    "1",
    "1",
    "1",
    "1",
    "1",
    "1",
    "1",
]


def hacer_pregunta(url, usuario_id, pregunta):
    body = json.dumps({"mensaje": pregunta, "usuario": f"prueba_{usuario_id}"}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    inicio = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp.read()
            status = resp.status
    except Exception as e:
        status = f"ERROR: {e}"
    duracion = time.time() - inicio
    return usuario_id, status, duracion


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url_posicional", nargs="?", default=None, help="URL base de la app (forma corta, sin --url)")
    parser.add_argument("--url", default=None, help="URL base de la app (sin /api/chat al final)")
    parser.add_argument("--usuarios", type=int, default=20, help="Cuántos usuarios simultáneos simular")
    args = parser.parse_args()

    url = args.url or args.url_posicional or "http://localhost:5000"

    endpoint = url.rstrip("/") + "/api/chat"
    print(f"Disparando {args.usuarios} preguntas EN PARALELO contra: {endpoint}\n")

    inicio_total = time.time()
    resultados = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.usuarios) as executor:
        futuros = [
            executor.submit(hacer_pregunta, endpoint, i, PREGUNTAS[i % len(PREGUNTAS)])
            for i in range(args.usuarios)
        ]
        for f in concurrent.futures.as_completed(futuros):
            resultados.append(f.result())
    total = time.time() - inicio_total

    resultados.sort(key=lambda r: r[0])
    exitosos = [r for r in resultados if r[1] == 200]
    fallidos = [r for r in resultados if r[1] != 200]

    print(f"{'usuario':<10}{'status':<20}{'tiempo (s)':<10}")
    for usuario_id, status, duracion in resultados:
        print(f"{usuario_id:<10}{str(status):<20}{duracion:.2f}")

    print("\n" + "=" * 45)
    print(f"Total: {len(resultados)} peticiones en {total:.2f}s (todas en paralelo)")
    print(f"Exitosas (200): {len(exitosos)}")
    print(f"Fallidas/timeout: {len(fallidos)}")
    if exitosos:
        tiempos = [r[2] for r in exitosos]
        print(f"Tiempo promedio: {statistics.mean(tiempos):.2f}s")
        print(f"Tiempo mínimo:   {min(tiempos):.2f}s")
        print(f"Tiempo máximo:   {max(tiempos):.2f}s")
    print("=" * 45)


if __name__ == "__main__":
    main()