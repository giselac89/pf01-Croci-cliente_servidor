import socket

host = "localhost"
port = 5000

#----------conexion al servidor----------
def conectar_servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
    except ConnectionRefusedError:
        print(f"El servidor no está corriendo en {host}:{port}")
        raise SystemExit(1)
    except socket.error as e:
        print(f"Error al conectar al servidor: {e}")
        raise SystemExit(1)

    print(f"Conectado al servidor en {host}:{port}")
    return s

 
#----------funcion para enviar mensaje al servidor----------

def enviar_mensaje(s):
    while True:
        mensaje = input("Ingrese un mensaje (o 'éxito' para terminar): ").strip()

        if not mensaje:
            print("No escribiste nada, probá de nuevo.")
            continue 
    
        if mensaje.lower() == "éxito":
            print("Cerrando conexión...")
            s.close()
            break
        try:
            s.send(mensaje.encode())
            print("Mensaje enviado al servidor.")
        except socket.error as e:
            print(f"Error al enviar el mensaje: {e}")
            break

        respuesta = s.recv(1024).decode()
        print(f"Respuesta del servidor: {respuesta}")


def main():
    s = conectar_servidor()
    try:
        enviar_mensaje(s)
    except KeyboardInterrupt:
        print("\nCerrando conexión...")
        s.close()

if __name__ == "__main__":
    main()