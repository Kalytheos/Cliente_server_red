import socket
import uuid

mac_address = ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 48, 8))
print(f"Dirección MAC de esta máquina: {mac_address}")

PROXY_HOST = "0.0.0.0"
PROXY_PORT = 4000
SERVER_IP = "172.17.0.3"
SERVER_PORT = 5000
TERMINAL_IP = "172.17.0.2"
TERMINAL_PORT = 5001
PALABRA_PROHIBIDA = "mala palabra"

terminal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.bind((PROXY_HOST, PROXY_PORT))
proxy_socket.listen(5)

print(f"Proxy escuchando en {PROXY_HOST}:{PROXY_PORT}...")

while True:
    client_conn, client_addr = proxy_socket.accept()
    client_ip, client_port = client_addr

    print(f"Cliente {client_ip}:{client_port} conectado al Proxy.")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((SERVER_IP, SERVER_PORT))

    # Mensaje de bienvenida al cliente
    client_conn.sendall("Conexión aceptada. Envía tu nombre.".encode("utf-8"))

    # Nombre del cliente
    client_name = client_conn.recv(1024).decode("utf-8")
    print(f"Cliente identificado como: {client_name}")
    terminal_socket.sendto(f"{client_name} se ha conectado al proxy".encode("utf-8"), (TERMINAL_IP, TERMINAL_PORT))

    # Enviar el nombre al servidor
    server_socket.sendall(client_name.encode("utf-8"))

    while True:
        data = client_conn.recv(1024).decode("utf-8")
        if not data or data.lower() == "exit":
            print(f"{client_name} ha cerrado la conexión.")
            break

        if data.strip() == PALABRA_PROHIBIDA:
            print(f"Mensaje bloqueado por el Proxy: '{data}'")
            client_conn.sendall("Mensaje bloqueado por contenido prohibido.".encode("utf-8"))
            continue

        print(f"Proxy reenvía el mensaje de {client_name} al servidor: {data}")
        server_socket.sendall(data.encode("utf-8"))

        # 🔹 Esperar respuesta del servidor
        confirmacion = server_socket.recv(1024).decode("utf-8")

        # 🔹 Enviar al cliente
        client_conn.sendall(confirmacion.encode("utf-8"))

        terminal_socket.sendto(
            f"Proxy ha reenviado el mensaje '{data}' de {client_name} al servidor".encode("utf-8"),
            (TERMINAL_IP, TERMINAL_PORT)
        )

    client_conn.close()
    server_socket.close()

proxy_socket.close()
terminal_socket.close()

