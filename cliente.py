import socket

host = "localhost"
port = 5000

#conexion al servidor
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

 
if __name__ == "__main__":
    conectar_servidor()