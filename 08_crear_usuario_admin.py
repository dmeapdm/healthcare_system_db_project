"""
🔐 SCRIPT DE INICIALIZACIÓN: primer usuario administrador
Hospital Heller - Electromedicina

QUÉ HACE:
Crea el primer registro en la tabla `users` con rol 'Ingeniero' asociado a
Hospital Heller (id_hospital = 1), con la contraseña hasheada con bcrypt
(nunca en texto plano).

REQUISITO PREVIO:
Haber corrido 07_security_rbac_audit.sql (deben existir las tablas
`roles`, `hospitals` y `users`).

CÓMO CORRERLO:
    pip install bcrypt mysql-connector-python python-dotenv --break-system-packages
    python 08_crear_usuario_admin.py
"""

import os
import getpass

import bcrypt
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar_base_datos():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def obtener_id_rol(cursor, nombre_rol):
    cursor.execute("SELECT id_role FROM roles WHERE role_name = %s;", (nombre_rol,))
    fila = cursor.fetchone()
    if fila is None:
        raise ValueError(f"El rol '{nombre_rol}' no existe en la tabla roles. ¿Corriste el script 07?")
    return fila[0]


def usuario_ya_existe(cursor, username):
    cursor.execute("SELECT id_user FROM users WHERE username = %s;", (username,))
    return cursor.fetchone() is not None


def crear_usuario_admin():
    print("=== Creación del primer usuario administrador (rol Ingeniero) ===")
    username = input("Nombre de usuario (login): ").strip()
    full_name = input("Nombre completo: ").strip()
    password = getpass.getpass("Contraseña: ")
    password_confirm = getpass.getpass("Confirmar contraseña: ")

    if password != password_confirm:
        print("❌ Las contraseñas no coinciden.")
        return
    if len(password) < 8:
        print("❌ La contraseña debe tener al menos 8 caracteres.")
        return

    # bcrypt.gensalt() genera un salt aleatorio distinto en cada llamada.
    # bcrypt.hashpw() lo combina con la contraseña y devuelve un hash que
    # YA INCLUYE el salt embebido (por eso no hace falta guardar el salt
    # en una columna aparte: viene "adentro" del string resultante).
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    conexion = conectar_base_datos()
    cursor = conexion.cursor()

    try:
        if usuario_ya_existe(cursor, username):
            print(f"❌ El usuario '{username}' ya existe.")
            return

        id_role = obtener_id_rol(cursor, "Ingeniero")
        id_hospital = 1  # Hospital Heller (Sede Principal) - creado en el script 07

        cursor.execute(
            """
            INSERT INTO users (username, password_hash, full_name, role_id, hospital_id, is_active)
            VALUES (%s, %s, %s, %s, %s, TRUE);
            """,
            (username, password_hash.decode("utf-8"), full_name, id_role, id_hospital),
        )
        conexion.commit()
        print(f"✅ Usuario '{username}' creado con rol Ingeniero en Hospital Heller (id_hospital=1).")

    except mysql.connector.Error as e:
        conexion.rollback()
        print(f"❌ Error de base de datos: {e}")
    finally:
        cursor.close()
        conexion.close()


if __name__ == "__main__":
    crear_usuario_admin()