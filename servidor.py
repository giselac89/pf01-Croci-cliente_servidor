
import socket
import sqlite3
from datetime import datetime


#----------configuracion del servidor----------
host = "localhost"
port = 5000
nombre_base_datos = "mensajes.db"

# funcion para crear socket TCP/IP
def crear_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP
    try:
        s.bind((host, port))    
    except OSError as error:
        print(f"ERROR - No se pudo iniciar el servidor: el puerto {port} ya está en uso.")
        print(f"Detalle técnico: {error}")
        raise SystemExit(1)
    
    s.listen()
    print("Esperando conexión...")
    return s

s = crear_socket()
conexion, direccion = s.accept()
print(f"Se conectó: {direccion}")

datos = conexion.recv(1024).decode()
print(f"Recibido: {datos}")

conexion.send("Mensaje recibido".encode())
conexion.close()
s.close()

