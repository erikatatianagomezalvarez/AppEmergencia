import mysql.connector
from mysql.connector import Error
from datetime import datetime

def main():
    host = "localhost"
    port = 3306
    user = "root"  # cambiar según entorno
    password = "12345678"  # cambiar por variable de entorno en producción
    database = "sistema_emergencias"

    try:
        conexion = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        if conexion.is_connected():
            print(f"Conexión exitosa a MySQL en el puerto {port}")

            cursor = conexion.cursor()

            insert_sql = """
            INSERT INTO tbusuario
            (idUsuario, cedulaUsuario, nombresApellidosUsuario, telefonoUsuario, contactoEmergenciaUsuario, tipoUsuario, direccionUsuario, emailUsuario, fechaRegistroUsuario, estadoUsuario)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            demo_values = (
                3,
                "1712345678",
                "Demo Usuario",
                "0987654321",
                "0999999999",
                "Paciente",
                "Calle Falsa 123",
                "demo@example.com",
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "Activo"
            )

            try:
                cursor.execute(insert_sql, demo_values)
                conexion.commit()
                print("Insert demo realizado correctamente. Filas afectadas:", cursor.rowcount)
            except Error as e:
                print("Error al insertar datos:", e)
            finally:
                cursor.close()

    except Error as error:
        print("Error al conectar a MySQL:", error)

    finally:
        if 'conexion' in locals() and conexion.is_connected():
            conexion.close()
            print("Conexión cerrada")


if __name__ == "__main__":
    main()