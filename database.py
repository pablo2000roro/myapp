import sqlite3
import pandas as pd

DB_NAME = "usuarios_api.db"

def conectar():
    return sqlite3.connect(DB_NAME)

# ✅ Crear tabla
def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
       CREATE TABLE IF NOT EXISTS usuarios(
           id INTEGER PRIMARY KEY,
           nombre TEXT,
           usuario TEXT,
           email TEXT,
           ciudad TEXT,
           telefono TEXT,
           sitio_web TEXT
       )
    """)

    conn.commit()
    conn.close()

# ✅ Guardar usuarios (CORREGIDO)
def guardar_usuarios(usuarios):
    conn = conectar()
    cursor = conn.cursor()

    for usuario in usuarios:
        cursor.execute("""
            INSERT OR IGNORE INTO usuarios
            (id, nombre, usuario, email, ciudad, telefono, sitio_web)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            usuario['id'],
            usuario['name'],                 # ✅ correcto
            usuario['username'],             # ✅ correcto
            usuario['email'],
            usuario['address']['city'],      # ✅ correcto
            usuario['phone'],
            usuario['website']
        ))

    conn.commit()   # ✅ fuera del for
    conn.close()

# ✅ Consultar usuarios
def consultar_usuarios():
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM usuarios", conn)
    conn.close()
    return df

# ✅ Eliminar datos
def eliminar_datos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios")
    conn.commit()
    conn.close()