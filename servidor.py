
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
        conn = sqlite3.connect(nombre_db)
    except sqlite3.OperationalError as e:
        print(f"ERROR - No se pudo acceder a la base de datos: {nombre_db}. Detalle técnico: {e}")
        raise SystemExit(1)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mensajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenido TEXT NOT NULL,
            fecha_envio TEXT NOT NULL,
            ip_cliente TEXT NOT NULL
        )
    """)
    conn.commit()  # Confirma la creación de la tabla en el archivo .db

    print(f"[OK] Base de datos '{nombre_db}' lista.")
    return conn


#prueba de las funciones antes de integrarlas

if __name__ == "__main__":
    s = crear_socket()
    conn = inicializar_base_datos()
    print("Ambas funciones corrieron sin errores.")
    s.close()
    conn.close()