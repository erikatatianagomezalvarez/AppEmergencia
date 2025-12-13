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


def get_all_tipoemergencia():
    """Devuelve todos los registros de `tbtipoemergencia` como lista de dicts."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT idTipoEmergencia, nombreTipoEmergencia, descripcionTipoEmergencia, nivelPrioridadTipoEmergencia_3, estadoTipoEmergencia_4 FROM tbtipoemergencia ORDER BY idTipoEmergencia"
        )
        rows = cursor.fetchall()
        return rows
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_tipoemergencia(tipo_id):
    """Devuelve un registro por `idTipoEmergencia` como diccionario o None."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT idTipoEmergencia, nombreTipoEmergencia, descripcionTipoEmergencia, nivelPrioridadTipoEmergencia_3, estadoTipoEmergencia_4 FROM tbtipoemergencia WHERE idTipoEmergencia = %s",
            (tipo_id,)
        )
        return cursor.fetchone()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def insert_tipoemergencia(nombre, descripcion, nivel, estado):
    """Inserta un nuevo tipo de emergencia y devuelve el id insertado."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO tbtipoemergencia
        (nombreTipoEmergencia, descripcionTipoEmergencia, nivelPrioridadTipoEmergencia_3, estadoTipoEmergencia_4)
        VALUES (%s,%s,%s,%s)
        """
        cursor.execute(sql, (nombre, descripcion, nivel, estado))
        conn.commit()
        return cursor.lastrowid
    except Error:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def update_tipoemergencia(tipo_id, nombre, descripcion, nivel, estado):
    """Actualiza un tipo de emergencia. Devuelve el número de filas afectadas."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        UPDATE tbtipoemergencia
        SET nombreTipoEmergencia=%s, descripcionTipoEmergencia=%s, nivelPrioridadTipoEmergencia_3=%s, estadoTipoEmergencia_4=%s
        WHERE idTipoEmergencia=%s
        """
        cursor.execute(sql, (nombre, descripcion, nivel, estado, tipo_id))
        conn.commit()
        return cursor.rowcount
    except Error:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def delete_tipoemergencia(tipo_id):
    """Elimina un tipo de emergencia. Devuelve filas afectadas."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbtipoemergencia WHERE idTipoEmergencia = %s", (tipo_id,))
        conn.commit()
        return cursor.rowcount
    except Error:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_all_servicioemergencia():
    """Devuelve todos los registros de `tbservicioemergencia` como lista de dicts."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT idServicioEmergencia, nombreServicioEmergencia, tipoServicioEmergencia, telefonoServicioEmergencia, disponibilidadServicioEmergencia, direccionBaseServicioEmergencia, capacidadAtencionServicioEmergencia, horarioServicioEmergencia, especialidadServicioEmergencia, estadoServicioEmergencia FROM tbservicioemergencia ORDER BY idServicioEmergencia"
        )
        rows = cursor.fetchall()
        return rows
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_servicioemergencia(servicio_id):
    """Devuelve un registro por `idServicioEmergencia` como diccionario o None."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT idServicioEmergencia, nombreServicioEmergencia, tipoServicioEmergencia, telefonoServicioEmergencia, disponibilidadServicioEmergencia, direccionBaseServicioEmergencia, capacidadAtencionServicioEmergencia, horarioServicioEmergencia, especialidadServicioEmergencia, estadoServicioEmergencia FROM tbservicioemergencia WHERE idServicioEmergencia = %s",
            (servicio_id,)
        )
        return cursor.fetchone()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def insert_servicioemergencia(nombre, tipo, telefono, disponibilidad, direccion, capacidad, horario, especialidad, estado):
    """Inserta un nuevo servicio de emergencia y devuelve el id insertado."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO tbservicioemergencia
        (nombreServicioEmergencia, tipoServicioEmergencia, telefonoServicioEmergencia, disponibilidadServicioEmergencia, direccionBaseServicioEmergencia, capacidadAtencionServicioEmergencia, horarioServicioEmergencia, especialidadServicioEmergencia, estadoServicioEmergencia)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (nombre, tipo, telefono, disponibilidad, direccion, capacidad, horario, especialidad, estado))
        conn.commit()
        return cursor.lastrowid
    except Error:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def update_servicioemergencia(servicio_id, nombre, tipo, telefono, disponibilidad, direccion, capacidad, horario, especialidad, estado):
    """Actualiza un servicio de emergencia. Devuelve el número de filas afectadas."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        UPDATE tbservicioemergencia
        SET nombreServicioEmergencia=%s, tipoServicioEmergencia=%s, telefonoServicioEmergencia=%s, disponibilidadServicioEmergencia=%s, direccionBaseServicioEmergencia=%s, capacidadAtencionServicioEmergencia=%s, horarioServicioEmergencia=%s, especialidadServicioEmergencia=%s, estadoServicioEmergencia=%s
        WHERE idServicioEmergencia=%s
        """
        cursor.execute(sql, (nombre, tipo, telefono, disponibilidad, direccion, capacidad, horario, especialidad, estado, servicio_id))
        conn.commit()
        return cursor.rowcount
    except Error:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def delete_servicioemergencia(servicio_id):
    """Elimina un servicio de emergencia. Devuelve filas afectadas."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbservicioemergencia WHERE idServicioEmergencia = %s", (servicio_id,))
        conn.commit()
        return cursor.rowcount
    except Error:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
