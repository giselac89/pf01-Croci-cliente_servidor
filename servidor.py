
import socket
import sqlite3
from datetime import datetime


#----------Configuración variables----------
host = "localhost"
port = 5000
nombre_db = "mensajes.db"

#----------Configuración del socket TCP/IP)----------
def crear_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP
    try:
        s.bind((host, port))    
    except OSError as error:
        print(f"ERROR - No se pudo iniciar el servidor: el puerto {port} ya está en uso.") #Manejo del error de "puerto ocupado"
        print(f"Detalle técnico: {error}")
        raise SystemExit(1)
    
    s.listen()
    print("Esperando conexión...")
    return s

#----------Inicialización de la base de datos----------
#        Conecta o crea la base de datos SQLite

def inicializar_base_datos():
    try:
        conexion_db = sqlite3.connect(nombre_db)
    except sqlite3.OperationalError as e:
        print(f"ERROR - No se pudo acceder a la base de datos: {nombre_db}. Detalle técnico: {e}")
        raise SystemExit(1)

    cursor = conexion_db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT NOT NULL,
            fecha_envio TEXT NOT NULL,
            ip_cliente TEXT NOT NULL
        )
    """)
    conexion_db.commit()  # Confirma la creación de la tabla en el archivo .db

    print(f"[OK] Base de datos '{nombre_db}' lista.")
    return conexion_db

#----------Función para guardar mensajes en la base de datos----------
def guardar_mensaje(conexion_db, contenido, fecha_envio, ip_cliente):
    try:
        cursor = conexion_db.cursor()
        cursor.execute("""
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        """, (contenido, fecha_envio, ip_cliente))
        conexion_db.commit()  # Confirma la inserción del mensaje en la base de datos
        return True
    except sqlite3.OperationalError as e:
        print(f"ERROR - No se pudo guardar el mensaje en la base de datos: {e}")
        return False

    
#----------Atender la conexión con un cliente----------

def atender_cliente(conexion, direccion, conexion_db):

    ip_cliente = direccion[0]  # direccion es ip + puerto 
    print(f"[INFO] Cliente conectado desde {ip_cliente}")

    while True:
        datos = conexion.recv(1024)
        if not datos:
            print("Cliente se desconectó.")
            break

        contenido = datos.decode()
        print(f"Mensaje recibido: {contenido}")  # mensaje recibido

        fecha_envio = datetime.now().isoformat()  # Timestamp actual
        guardar_mensaje(conexion_db, contenido, fecha_envio, direccion[0])

        respuesta = f"Mensaje recibido: {fecha_envio}"
        conexion.send(respuesta.encode())

    conexion.close()


#----------Programa principal----------
def main():
    socket = crear_socket()
    conexion_db = inicializar_base_datos()

    try:
        while True:
            conexion, direccion = socket.accept()
            atender_cliente(conexion, direccion, conexion_db)
            print("Esperando conexión...")
    except KeyboardInterrupt:
        print("\nServidor detenido manualmente (Ctrl+C).")
    finally:
        socket.close()
        conexion_db.close()
        print("Servidor cerrado.")


if __name__ == "__main__":
    main()