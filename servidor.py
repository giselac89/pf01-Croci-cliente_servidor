
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET = IPv4, SOCK_STREAM = TCP
s.bind(("localhost", 5000))
s.listen()
print("Esperando conexión...")

conexion, direccion = s.accept()
print(f"Se conectó: {direccion}")

datos = conexion.recv(1024).decode()
print(f"Recibido: {datos}")

conexion.send("Mensaje recibido".encode())
conexion.close()
s.close()
