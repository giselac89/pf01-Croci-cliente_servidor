import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 5000))
s.send("Hola servidor".encode())

respuesta = s.recv(1024).decode()
print(f"El servidor dijo: {respuesta}")

