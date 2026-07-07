# Scripts de utilidad (uso puntual, no se ejecutan en producción)

- `agregar_columna.py`: script que se usó una vez para agregar una columna a la base de datos.
- `mejorar_db.py`: script que se usó una vez para migrar/mejorar el esquema de la base de datos.

Ninguno de los dos lo importa `app.py` ni ningún otro módulo del sistema en tiempo
de ejecución. Se guardan aquí (en vez de borrarlos) por si necesitas repetir esa
migración en otro ambiente. Si ya no los necesitas, puedes borrar esta carpeta
completa sin que nada se rompa.
