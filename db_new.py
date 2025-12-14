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
        tipo = kwargs.get('tipo', '')
        direccion = kwargs.get('direccion', '')
        estado = kwargs.get('estado', 'activo')
        fecha = kwargs.get('fecha', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        cursor.execute(insert_sql, (cedula, name, telefono, contacto, tipo, direccion, email, fecha, estado))
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


def get_user(user_id):
    """Devuelve un usuario por id o None si no existe."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbusuario WHERE idUsuario = %s", (user_id,))
        return cursor.fetchone()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def update_user(user_id, cedula, nombre, telefono, contacto, tipo, direccion, email, fecha, estado):
    """Actualiza un usuario."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        UPDATE tbusuario SET
        cedulaUsuario=%s, nombresApellidosUsuario=%s, telefonoUsuario=%s,
        contactoEmergenciaUsuario=%s, tipoUsuario=%s, direccionUsuario=%s,
        emailUsuario=%s, fechaRegistroUsuario=%s, estadoUsuario=%s
        WHERE idUsuario=%s
        """
        cursor.execute(sql, (cedula, nombre, telefono, contacto, tipo, direccion, email, fecha, estado, user_id))
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


def delete_user(user_id):
    """Elimina un usuario."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbusuario WHERE idUsuario = %s", (user_id,))
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


def get_all_tipoemergencia():
    """Devuelve todos los tipos de emergencia."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbtipoemergencia")
        return cursor.fetchall()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_tipoemergencia(tipo_id):
    """Devuelve un tipo de emergencia por id."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbtipoemergencia WHERE idTipoEmergencia = %s", (tipo_id,))
        return cursor.fetchone()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def insert_tipoemergencia(nombre, descripcion, nivel, estado):
    """Inserta un nuevo tipo de emergencia."""
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
    """Actualiza un tipo de emergencia."""
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
    """Elimina un tipo de emergencia."""
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
    """Devuelve todos los servicios de emergencia."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbservicioemergencia")
        return cursor.fetchall()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_servicioemergencia(servicio_id):
    """Devuelve un servicio de emergencia por id."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbservicioemergencia WHERE idServicioEmergencia = %s", (servicio_id,))
        return cursor.fetchone()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def insert_servicioemergencia(nombre, tipo, telefono, disponibilidad, direccion, capacidad, horario, especialidad, estado):
    """Inserta un nuevo servicio de emergencia."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO tbservicioemergencia
        (nombreServicioEmergencia, tipoServicioEmergencia, telefonoServicioEmergencia, disponibilidadServicioEmergencia, direccionServicioEmergencia, capacidadServicioEmergencia, horarioServicioEmergencia, especialidadServicioEmergencia, estadoServicioEmergencia)
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
    """Actualiza un servicio de emergencia."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        UPDATE tbservicioemergencia
        SET nombreServicioEmergencia=%s, tipoServicioEmergencia=%s, telefonoServicioEmergencia=%s, disponibilidadServicioEmergencia=%s, direccionServicioEmergencia=%s, capacidadServicioEmergencia=%s, horarioServicioEmergencia=%s, especialidadServicioEmergencia=%s, estadoServicioEmergencia=%s
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
    """Elimina un servicio de emergencia."""
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


def get_all_contactoemergencia():
    """Devuelve todos los contactos de emergencia."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbcontactoemergencia")
        return cursor.fetchall()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_contactoemergencia(contacto_id):
    """Devuelve un contacto de emergencia por id."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tbcontactoemergencia WHERE idContactoEmergencia = %s", (contacto_id,))
        return cursor.fetchone()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def insert_contactoemergencia(tipo_id, nombre, telefono, tipo, descripcion, estado):
    """Inserta un nuevo contacto de emergencia."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO tbcontactoemergencia
        (tbTipoEmergencia_idTipoEmergencia, nombreContactoEmergencia, telefonoContactoEmergencia, tipoContactoEmergencia, descripcionContactoEmergencia, estadoContactoEmergencia)
        VALUES (%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (tipo_id, nombre, telefono, tipo, descripcion, estado))
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


def update_contactoemergencia(contacto_id, tipo_id, nombre, telefono, tipo, descripcion, estado):
    """Actualiza un contacto de emergencia."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        UPDATE tbcontactoemergencia
        SET tbTipoEmergencia_idTipoEmergencia=%s, nombreContactoEmergencia=%s, telefonoContactoEmergencia=%s, tipoContactoEmergencia=%s, descripcionContactoEmergencia=%s, estadoContactoEmergencia=%s
        WHERE idContactoEmergencia=%s
        """
        cursor.execute(sql, (tipo_id, nombre, telefono, tipo, descripcion, estado, contacto_id))
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


def delete_contactoemergencia(contacto_id):
    """Elimina un contacto de emergencia."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbcontactoemergencia WHERE idContactoEmergencia = %s", (contacto_id,))
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


def get_all_emergencia():
    """Devuelve todos los registros de `tbemergencia` como lista de dicts."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT idEmergencia, tbUsuario_idUsuario, tbTipoEmergencia_idTipoEmergencia, codigoEmergencia, fechaHoraEmergencia, tipoEmergencia, estadoEmergencia, ubicacionEmergencia, latitudEmergencia, longitudEmergencia, descripcionEmergencia, prioridadEmergencia, idusuarioreportaEmergencia, fechaCierreEmergencia, observacionesEmergencia FROM tbemergencia ORDER BY idEmergencia"
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


def get_emergencia(emergencia_id):
    """Devuelve un registro por `idEmergencia` como diccionario o None."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT idEmergencia, tbUsuario_idUsuario, tbTipoEmergencia_idTipoEmergencia, codigoEmergencia, fechaHoraEmergencia, tipoEmergencia, estadoEmergencia, ubicacionEmergencia, latitudEmergencia, longitudEmergencia, descripcionEmergencia, prioridadEmergencia, idusuarioreportaEmergencia, fechaCierreEmergencia, observacionesEmergencia FROM tbemergencia WHERE idEmergencia = %s",
            (emergencia_id,)
        )
        return cursor.fetchone()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def insert_emergencia(usuario_id, tipoemergencia_id, codigo, fecha_hora, tipo, estado, ubicacion, latitud, longitud, descripcion, prioridad, idusuarioreporta, fecha_cierre, observaciones):
    """Inserta una nueva emergencia y devuelve el id insertado."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO tbemergencia
        (tbUsuario_idUsuario, tbTipoEmergencia_idTipoEmergencia, codigoEmergencia, fechaHoraEmergencia, tipoEmergencia, estadoEmergencia, ubicacionEmergencia, latitudEmergencia, longitudEmergencia, descripcionEmergencia, prioridadEmergencia, idusuarioreportaEmergencia, fechaCierreEmergencia, observacionesEmergencia)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (usuario_id, tipoemergencia_id, codigo, fecha_hora, tipo, estado, ubicacion, latitud, longitud, descripcion, prioridad, idusuarioreporta, fecha_cierre, observaciones))
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


def update_emergencia(emergencia_id, usuario_id, tipoemergencia_id, codigo, fecha_hora, tipo, estado, ubicacion, latitud, longitud, descripcion, prioridad, idusuarioreporta, fecha_cierre, observaciones):
    """Actualiza una emergencia. Devuelve el número de filas afectadas."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        UPDATE tbemergencia
        SET tbUsuario_idUsuario=%s, tbTipoEmergencia_idTipoEmergencia=%s, codigoEmergencia=%s, fechaHoraEmergencia=%s, tipoEmergencia=%s, estadoEmergencia=%s, ubicacionEmergencia=%s, latitudEmergencia=%s, longitudEmergencia=%s, descripcionEmergencia=%s, prioridadEmergencia=%s, idusuarioreportaEmergencia=%s, fechaCierreEmergencia=%s, observacionesEmergencia=%s
        WHERE idEmergencia=%s
        """
        cursor.execute(sql, (usuario_id, tipoemergencia_id, codigo, fecha_hora, tipo, estado, ubicacion, latitud, longitud, descripcion, prioridad, idusuarioreporta, fecha_cierre, observaciones, emergencia_id))
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


def delete_emergencia(emergencia_id):
    """Elimina una emergencia. Devuelve filas afectadas."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbemergencia WHERE idEmergencia = %s", (emergencia_id,))
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


# CRUD para tbhistorialestados
def get_all_historialestados():
    """Devuelve todos los registros del historial de estados."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT idHistorialEstados, tbEmergencia_idEmergencia, tbUsuario_idUsuario, estadoAnterior, estadoNuevo, fechaCambioHistorialEstados, usuarioCambioHistorialEstados, motivoHistorialEstados FROM tbhistorialestados ORDER BY fechaCambioHistorialEstados DESC"
        )
        return cursor.fetchall()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_historialestados(historial_id):
    """Devuelve un registro del historial por id."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT idHistorialEstados, tbEmergencia_idEmergencia, tbUsuario_idUsuario, estadoAnterior, estadoNuevo, fechaCambioHistorialEstados, usuarioCambioHistorialEstados, motivoHistorialEstados FROM tbhistorialestados WHERE idHistorialEstados = %s",
            (historial_id,)
        )
        return cursor.fetchone()
    except Error:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def insert_historialestados(emergencia_id, usuario_id, estado_anterior, estado_nuevo, fecha_cambio, usuario_cambio, motivo):
    """Inserta un nuevo registro de historial de estados."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO tbhistorialestados
        (tbEmergencia_idEmergencia, tbUsuario_idUsuario, estadoAnterior, estadoNuevo, fechaCambioHistorialEstados, usuarioCambioHistorialEstados, motivoHistorialEstados)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (emergencia_id, usuario_id, estado_anterior, estado_nuevo, fecha_cambio, usuario_cambio, motivo))
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


def update_historialestados(historial_id, emergencia_id, usuario_id, estado_anterior, estado_nuevo, fecha_cambio, usuario_cambio, motivo):
    """Actualiza un registro del historial."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
        UPDATE tbhistorialestados
        SET tbEmergencia_idEmergencia=%s, tbUsuario_idUsuario=%s, estadoAnterior=%s, estadoNuevo=%s, fechaCambioHistorialEstados=%s, usuarioCambioHistorialEstados=%s, motivoHistorialEstados=%s
        WHERE idHistorialEstados=%s
        """
        cursor.execute(sql, (emergencia_id, usuario_id, estado_anterior, estado_nuevo, fecha_cambio, usuario_cambio, motivo, historial_id))
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


def delete_historialestados(historial_id):
    """Elimina un registro del historial."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbhistorialestados WHERE idHistorialEstados = %s", (historial_id,))
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
