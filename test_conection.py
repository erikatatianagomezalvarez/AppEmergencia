import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="localhost",
        port=3306,             # ← tu puerto
        user="root",     # ← cambia esto
        password="12345678",# ← cambia esto
        database="sistema_emergencias"     # ← cambia esto
    )

    if conexion.is_connected():
        print("Conexión exitosa a MySQL en el puerto 3386")

except mysql.connector.Error as error:
    print("Error al conectar a MySQL:", error)

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("Conexión cerrada")