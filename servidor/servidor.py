import socket
import uuid

mac_address = ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 48, 8))
print(f"Dirección MAC de esta máquina: {mac_address}")

HOST = "0.0.0.0"
PORT = 5000
BANNED_PORT = 6000
TERMINAL_IP = "172.17.0.2"
TERMINAL_PORT = 5001

terminal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Servidor escuchando en {HOST}:{PORT}...")

while True:
    conn, addr = server_socket.accept()
    client_ip, client_port = addr

    if client_port == BANNED_PORT:
        mensaje_rechazo = f"Conexión rechazada desde {client_ip}:{client_port} (Puerto Bloqueado)"
        print(mensaje_rechazo)
        conn.sendall(f"Conexión rechazada: No puedes usar el puerto {BANNED_PORT}.".encode("utf-8"))
        conn.close()
        terminal_socket.sendto(mensaje_rechazo.encode("utf-8"), (TERMINAL_IP, TERMINAL_PORT))
        continue

    #conn.sendall("Conexión aceptada. Envía tu nombre.".encode("utf-8"))

    client_name = conn.recv(1024).decode("utf-8")
    print(f"Cliente conectado desde {client_ip} con nombre {client_name}")

    terminal_socket.sendto(
        f"{client_name} se ha conectado al servidor desde {client_ip}".encode("utf-8"),
        (TERMINAL_IP, TERMINAL_PORT)
    )

    while True:
        data = conn.recv(1024).decode("utf-8")
        if not data or data.lower() == "exit":
            print(f"{client_name} ({client_ip}) ha cerrado la conexión.")
            break

        print(f"Mensaje recibido de '{client_ip}', con nombre '{client_name}': {data}")

        terminal_socket.sendto(
            f"Servidor ha recibido de '{client_name}' el mensaje '{data}'".encode("utf-8"),
            (TERMINAL_IP, TERMINAL_PORT)
        )

        confirmacion = f"Mensaje recibido: {data}"
        conn.sendall(confirmacion.encode("utf-8"))

    conn.close()

server_socket.close()
terminal_socket.close()

