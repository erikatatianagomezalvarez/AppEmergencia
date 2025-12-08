import os
from datetime import datetime

import mysql.connector
from mysql.connector import Error


def get_connection():
    """Crea y devuelve una conexión a la base de datos MySQL.

    Los valores pueden configurarse con variables de entorno:
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
    """
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '3306')),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '12345678'),
        database=os.getenv('DB_NAME', 'sistema_emergencias')
    )


def get_all_users():
    """Devuelve lista de usuarios (diccionarios) desde `tbusuario`."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT idUsuario, nombresApellidosUsuario, emailUsuario, telefonoUsuario FROM tbusuario"
        )
        rows = cursor.fetchall()
        return rows
    except Error as e:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def ensure_auto_increment(start=4):
    """Asegura que `tbusuario` tenga AUTO_INCREMENT al menos en `start`.

    Si el máximo `idUsuario` existente es menor que `start`, se ejecuta
    `ALTER TABLE tbusuario AUTO_INCREMENT = start`.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(idUsuario) FROM tbusuario")
        row = cursor.fetchone()
        max_id = row[0] if row else None

        if max_id is None:
            # tabla vacía -> podemos establecer AUTO_INCREMENT
            cursor.execute(f"ALTER TABLE tbusuario AUTO_INCREMENT = {int(start)}")
            conn.commit()
        else:
            try:
                current = int(max_id)
            except Exception:
                current = 0
            if current < int(start):
                cursor.execute(f"ALTER TABLE tbusuario AUTO_INCREMENT = {int(start)}")
                conn.commit()
    except Error:
        # No forzamos fallo aquí; al fallar la alteración, la inserción intentará de todas formas.
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def insert_user(name, email, telefono, **kwargs):
    """Inserta un nuevo usuario en `tbusuario`.

    No incluye `idUsuario` en el INSERT para permitir AUTO_INCREMENT.
    Devuelve el id insertado (lastrowid).
    """
    conn = None
    cursor = None
    try:
        # Asegurar auto-increment mínimo antes de insertar
        ensure_auto_increment(4)

        conn = get_connection()
        cursor = conn.cursor()

        insert_sql = """
        INSERT INTO tbusuario
        (cedulaUsuario, nombresApellidosUsuario, telefonoUsuario, contactoEmergenciaUsuario, tipoUsuario, direccionUsuario, emailUsuario, fechaRegistroUsuario, estadoUsuario)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cedula = kwargs.get('cedula', '')
        contacto = kwargs.get('contacto', '')
        tipo = kwargs.get('tipo', 'Paciente')
        direccion = kwargs.get('direccion', '')
        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        estado = kwargs.get('estado', 'Activo')

        values = (cedula, name, telefono, contacto, tipo, direccion, email, fecha, estado)

        cursor.execute(insert_sql, values)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
