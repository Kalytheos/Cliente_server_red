import socket
import uuid

mac_address = ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 48, 8))
print(f"Dirección MAC de esta máquina: {mac_address}")

# Configuración de la Terminal
HOST = "0.0.0.0"
PORT = 5001

# Crear socket UDP para recibir mensajes
terminal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
terminal_socket.bind((HOST, PORT))

print(f"Terminal escuchando en {HOST}:{PORT}...\n")
print(f"Cliente <---> Proxy usando protocolo TCP... \n")
print(f"Proxy <---> Servidor usando protocolo TCP... \n")
print(f"Terminal usando protocolo UDP... \n")

while True:
    data, addr = terminal_socket.recvfrom(1024)
    mensaje = data.decode("utf-8")
    
    if "se ha conectado al servidor" in mensaje:
        print(f"[CONEXIÓN] {mensaje}")
    elif "ha enviado el mensaje" in mensaje:
        print(f"[MENSAJE] {mensaje}")
    elif "Conexión rechazada" in mensaje:
        print(f"[RECHAZO] {mensaje}")
    else:
        print(f"[INFO] {mensaje}")

